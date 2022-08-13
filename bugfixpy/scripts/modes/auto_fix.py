"""
Automatic bug fix mode. Takes in a challenge ID and scrapes the CMS to retrieve all Jira issue data
to avoid more user input. Automatically transitions tickets in Jira
"""


import sys
from bugfixpy import jira_api
from bugfixpy.scraper import CmsScraper
from bugfixpy.constants import colors, headers, instructions
from bugfixpy.gitrepository import GitRepository
from bugfixpy.scripts import transition
from bugfixpy.scripts.git import fix_branches_in_repository
from bugfixpy.formatter import Text
from bugfixpy.utils import user_input
from bugfixpy.scripts.cms import scrape_cms


def run(test_mode: bool) -> None:
    """
    Main bug fixing function. Checks the mode, scrapes the CMS, opens the
    repository, and walks the user through the steps to fix the bug in all
    branches necessary.
    """
    Text(headers.AUTO_MODE_ENABLED, colors.HEADER).display()

    if test_mode:
        Text(headers.TEST_MODE, colors.HEADER).display()

    # Otherwise check if credentials are valid
    elif not jira_api.has_valid_credentials():
        Text(
            "Invalid API credentials. Run with --setup to change credentials",
            colors.FAIL,
        ).display()
        sys.exit(1)

    challenge_id = user_input.get_challenge_id()

    print("Collecting data from CMS...", end="")

    # Create Scraper instance
    scraper = CmsScraper(challenge_id)

    # Attempt to scrape CMS and retrieve data
    scraper_data = scrape_cms(scraper)

    Text("[Done]", colors.OKGREEN).display()

    print("Cloning Repository...", end="")

    # Attempt to create repository
    try:
        repository = GitRepository(scraper_data.application.repository_name)
    except ValueError:
        Text("Error getting repository", colors.FAIL).display()
        sys.exit(1)

    Text("[Done]", colors.OKGREEN).display()

    # Print CMS details from scraper
    Text("Application CHLC:", scraper_data.application.chlc, colors.OKCYAN).display()
    Text("Challenge CHLC:", scraper_data.challenge.chlc, colors.OKCYAN).display()

    # Print repository details from GitRepository
    Text("Repo:", scraper_data.application.repository_name, colors.OKCYAN).display()
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

    try:
        # Automatically transition jira tickets
        transition.transition_jira_issues(
            fix_messages,
            repo_was_cherrypicked,
            scraper_data.challenge.chlc,
            scraper_data.application.chlc,
        )

    except Exception as err:
        print(err)
        sys.exit(1)

    # Notify user to check chunks if lines were added
    if is_chunk_fixing_required:
        print(instructions.UPDATE_CMS_AND_FIX_CHUNKS_REMINDER)
    else:
        print(instructions.UPDATE_CMS_REMINDER)

    print(instructions.BUG_FIX_COMPLETE)
