import webbrowser
from src.scraper import CmsScraper
from src.git import GitRepository
from src import utils, api, constants, exceptions
from src.constants import colors, headers, instructions
from src.utils import Text

# Main function runs bug-fix program
def main(auto_mode, test_mode):
    """
    Main bug fixing function. Checks the mode, scrapes the CMS, opens the repository,
    and walks the user through the steps to fix the bug in all branches necessary.
    """
    if test_mode:
        print(Text(headers.TEST_MODE, colors.HEADER))
    if auto_mode:
        Text(headers.AUTO_MODE_ENABLED, colors.HEADER)
    else:
        Text(headers.AUTO_MODE_DISABLED, colors.HEADER)

    #
    # Move this to new validate credentials method that returns true/false and prints out what is not present
    #
    # Check if environment variables do not exist
    if not test_mode and auto_mode and (not constants.JIRA_API_EMAIL or not constants.JIRA_API_KEY or not constants.CMS_EMAIL or not constants.CMS_PASSWORD):
        print(f'{constants.FAIL}Credentials not setup. Run \'bug-fix.py --setup\' to set up environment variables{constants.ENDC}')

        # Notify that no email is present
        if not constants.JIRA_API_EMAIL:
            print(f'{constants.FAIL}No API email present{constants.ENDC}')

        # Notify that no api key is present
        if not constants.JIRA_API_KEY:
            print(f'{constants.FAIL}No API key present{constants.ENDC}')

        # Notify that no email is present
        if not constants.CMS_EMAIL:
            print(f'{constants.FAIL}No CMS email present{constants.ENDC}')

        # Notify that no api key is present
        if not constants.CMS_PASSWORD:
            print(f'{constants.FAIL}No CMS password present{constants.ENDC}')

        exit(1)

    # Check if API credentials are valid, otherwise exit program
    if not test_mode and auto_mode and not api.has_valid_credentials():
        print(f'{constants.FAIL}Invalid API credentials. Run with --setup to change credentials{constants.ENDC}')
        exit(1)

    #######Get challenge id input and validate it first######

    challenge_id = input('Enter Challenge ID: ')

    while not utils.is_valid_cid(challenge_id):
        print('Invalid Challenge ID. Try again')
        challenge_id = input('Enter Challenge ID: ')

    #########################################################
    # Validate that all credentials work before scraping
    # Handle errors with CmsScraper better. Try except blocks?

    # Attempt to scrape CMS to get data
    try:
        scraper = CmsScraper(challenge_id)
    except ValueError as e:
        print(e)
        exit(1)
    except exceptions.RequestFailedError as e:
        print(e)
        exit(1)

    # Get data from scraper
    application_chlc = scraper.get_application_chlc()
    challenge_chlc = scraper.get_challenge_chlc()
    repo_name = scraper.get_git_repo()

    print('Application CHLC:', application_chlc)
    print('Challenge CHLC:', challenge_chlc)

    # Attempt to create repository
    try:
        repository = GitRepository(repo_name)
    except ValueError as e:
        print(e)
        exit(1)

    # Print Details about the repository
    print(f'Repo:{constants.OKCYAN} {repo_name}{constants.ENDC}')
    print(f'Branches:{constants.OKCYAN} {repository.get_num_branches()}{constants.ENDC}')

    if repository.get_is_full_app():
        print(f'Type: {constants.OKCYAN}Full App{constants.ENDC}')
    else:
        print(f'Type: {constants.OKCYAN}Minified App{constants.ENDC}')

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
