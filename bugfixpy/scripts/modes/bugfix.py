import sys
from bugfixpy import exceptions, jira_api
from bugfixpy.scraper import CmsScraper
from bugfixpy.constants import colors, headers, instructions
from bugfixpy.gitrepository import GitRepository
from bugfixpy.scripts import transition
from bugfixpy.scripts.fixallbranches import fix_branches_in_repository
from bugfixpy.formatting import Text
from bugfixpy.utils import user_input


def run(test_mode: bool) -> None:
    """
    Main bug fixing function. Checks the mode, scrapes the CMS, opens the
    repository, and walks the user through the steps to fix the bug in all
    branches necessary.
    """
    Text(headers.AUTO_MODE_ENABLED, colors.HEADER).display()

    if test_mode:
        print(Text(headers.TEST_MODE, colors.HEADER))

    # Check if API credentials are valid, otherwise exit program
    if not test_mode and not jira_api.has_valid_credentials():
        Text(
            "Invalid API credentials. Run with --setup to change credentials",
            colors.FAIL,
        ).display()
        exit(1)

    challenge_id = user_input.get_challenge_id()

    print("Collecting data from CMS...", end="")

    # Attempt to scrape CMS to get data
    try:
        scraper = CmsScraper(challenge_id)
        scraper.scrape_cms()
    except ValueError as err:
        Text(f"\n{err}", colors.FAIL).display()
        sys.exit(1)
    except exceptions.RequestFailedError as err:
        Text(f"\n{err}", colors.FAIL).display()
        sys.exit(1)
    except Exception as err:
        Text("\nUnknown Error", err, colors.FAIL).display()
        sys.exit(1)

    Text("[Done]", colors.OKGREEN).display()

    # Get data from scraper
    application_chlc = scraper.get_application_chlc()
    challenge_chlc = scraper.get_challenge_chlc()
    repo_name = scraper.get_git_repo()

    # Attempt to create repository
    try:
        print("Cloning Repository...", end="")
        repository = GitRepository(repo_name)
        Text("[Done]", colors.OKGREEN).display()
    except ValueError:
        Text("Error getting repository", colors.FAIL).display()
        sys.exit(1)

    # Print CMS details from scraper
    Text("Application CHLC:", application_chlc, colors.OKCYAN).display()
    Text("Challenge CHLC:", challenge_chlc, colors.OKCYAN).display()

    # Print repository details from GitRepository
    Text("Repo:", repo_name, colors.OKCYAN).display()
    Text("Branches:", repository.get_num_branches(), colors.OKCYAN).display()

    if repository.is_full_app():
        Text("Type", "Full App", colors.OKCYAN).display()
    else:
        Text("Type:", "Minified App", colors.OKCYAN).display()

    # Run bug fix on repository
    fix_branches_in_repository(repository)

    # If test mode, don't push to repository
    if test_mode:
        input(instructions.PROMPT_FOR_ENTER_PUSH_DISABLED)
    else:
        input(instructions.PROMPT_FOR_ENTER_PUSH_ENABLED)

        # Push commit to the repository
        repository.push_fix_to_github()

    # Collect results from repository after running bug fix
    fix_messages = repository.get_fix_messages()
    repo_was_cherrypicked = repository.did_cherrypick_run()
    is_chunk_fixing_required = repository.did_number_of_lines_change()

    # If parameter not entered, prompt user for CHRLQ
    chlrq = user_input.get_chlrq()

    # Automatically transition jira tickets
    transition.transition_jira_issues(chlrq, fix_messages, repo_was_cherrypicked)

    # Notify user to check chunks if lines were added
    if is_chunk_fixing_required:
        print(instructions.UPDATE_CMS_AND_FIX_CHUNKS_REMINDER)
    else:
        print(instructions.UPDATE_CMS_REMINDER)

    print(instructions.BUG_FIX_COMPLETE)
