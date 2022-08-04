from src.scraper import CmsScraper
from src.git import GitRepository
from src import utils, api, constants, exceptions
from src.constants import colors, headers, instructions
from src.utils import Text

# Main function runs bug-fix program
def main(test_mode):
    """
    Main bug fixing function. Checks the mode, scrapes the CMS, opens the repository,
    and walks the user through the steps to fix the bug in all branches necessary.
    """
    Text(headers.AUTO_MODE_ENABLED, colors.HEADER).display()

    if test_mode:
        print(Text(headers.TEST_MODE, colors.HEADER))

    #
    # Move this to new validate credentials method that returns true/false and prints out what is not present
    #
    # Check if environment variables do not exist
    if not test_mode and (not constants.JIRA_API_EMAIL
                        or not constants.JIRA_API_KEY
                        or not constants.CMS_EMAIL
                        or not constants.CMS_PASSWORD):
        Text('Credentials not setup. Run \'bug-fix.py --setup\' to set up environment variables', colors.FAIL).display()

        # Notify that no email is present
        if not constants.JIRA_API_EMAIL:
            Text('No API email present', colors.FAIL).display()

        # Notify that no api key is present
        if not constants.JIRA_API_KEY:
            Text('No API key present', colors.FAIL).display()

        # Notify that no email is present
        if not constants.CMS_EMAIL:
            Text('No CMS email present', colors.FAIL).display()

        # Notify that no api key is present
        if not constants.CMS_PASSWORD:
            Text('No CMS password present', colors.FAIL).display()

        exit(1)

    # Check if API credentials are valid, otherwise exit program
    if not test_mode and not api.has_valid_credentials():
        Text('Invalid API credentials. Run with --setup to change credentials', colors.FAIL).display()
        exit(1)

    #######Get challenge id input and validate it first######

    challenge_id = input('Enter Challenge ID: ')

    while not utils.is_valid_cid(challenge_id):
        Text('Invalid Challenge ID. Try again', colors.FAIL).display()
        challenge_id = input('Enter Challenge ID: ')

    #########################################################
    # Validate that all credentials work before scraping
    # Handle errors with CmsScraper better. Try except blocks?

    # Attempt to scrape CMS to get data
    try:
        scraper = CmsScraper(challenge_id)
    except ValueError as e:
        Text(e, colors.FAIL).display()
        Text('CMS Error: Invalid Challenge ID', colors.FAIL).display()
        exit(1)
    except exceptions.RequestFailedError:
        Text(e, colors.FAIL).display()
        Text('CMS Error: Failed Request', colors.FAIL).display()
        exit(1)
    except Exception:
        Text('Unknown Error', colors.FAIL).display()

    # Get data from scraper
    application_chlc = scraper.get_application_chlc()
    challenge_chlc = scraper.get_challenge_chlc()
    repo_name = scraper.get_git_repo()

    # Attempt to create repository
    try:
        repository = GitRepository(repo_name)
    except ValueError as e:
        Text('Error getting repository', colors.FAIL).display()
        exit(1)

    # Print CMS details from scraper
    Text('Application CHLC:', application_chlc, colors.OKCYAN).display()
    Text('Challenge CHLC:', challenge_chlc, colors.OKCYAN).display()

    # Print repository details from GitRepository
    Text('Repo:', repo_name, colors.OKCYAN).display()
    Text('Branches:', repository.get_num_branches(), colors.OKCYAN).display()

    if repository.get_is_full_app():
        Text('Type', 'Full App', colors.OKCYAN).display()
    else:
        Text('Type:', 'Minified App', colors.OKCYAN).display()

    # Run bug fix on repository
    repository.run_bug_fix()

    # If test mode, don't push to repository
    if test_mode:
        input(instructions.PROMPT_FOR_ENTER_PUSH_DISABLED)
    else:
        input(instructions.PROMPT_FOR_ENTER_PUSH_ENABLED)
        
        # Push commit to the repository
        repository.push()

    # Collect results from repository after running bug fix
    fix_messages = repository.get_fix_messages()
    repo_was_cherrypicked = repository.did_cherrypick_run()
    is_chunk_fixing_required = repository.did_number_of_lines_change()

    # If parameter not entered, prompt user for CHRLQ
    chlrq = utils.get_chlrq()

    # Automatically transition jira tickets
    utils.transition_jira_issues(chlrq, utils.format_messages(fix_messages), repo_was_cherrypicked)

    # Notify user to check chunks if lines were added
    if is_chunk_fixing_required:
        print(instructions.UPDATE_CMS_AND_FIX_CHUNKS_REMINDER)
    else:
        print(instructions.UPDATE_CMS_REMINDER)

    print(instructions.BUG_FIX_COMPLETE)
