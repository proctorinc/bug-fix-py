import subprocess
import webbrowser
from src.scraper import CmsScraper
from src.git import GitRepository
from src import git, utils, api, constants

def is_valid_cid(challenge_id):
    return True

# Main function runs bug-fix program
def run(auto_mode, test_mode):

    # Parse commandline arguments
    args = utils.parse_arguments()

    # Default user is not done fixing branches
    done_fixing = False

    # Set default cherrypick has not occurred
    did_cherrypick = False

    # Hold fix messages for all branches in list
    fix_messages = []

    # Track whether chunks need to be fixed or not
    fix_chunks_required = False

    # # define variables from arguments
    # test_mode = args.test
    # only_transition_mode = args.transition
    # auto_mode = args.api
    # debug = args.debug

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

    #
    # Choice between starting with CID and application? 
    #
#####GIT#REPOSITORY#######################################################

    # # This will come from the webscraper
    # repo_name = 'opentasks'

    # try:
    #     repository = GitRepository(repo_name)
    # except ValueError as e:
    #     print(e)
    #     exit(1)

#####SCRAPER##############################################################
    challenge_id = input('Enter Challenge ID: ')

    while not is_valid_cid(challenge_id):
        print('Invalid Challenge ID. Try again')
        challenge_id = input('Enter Challenge ID: ')

    # Validate that all credentials work before scraping
    # Handle errors with CmsScraper better. Try except blocks?
    try:
        scraper = CmsScraper(challenge_id)
    except ValueError as e:
        print(e)
        exit(1)

    print('App CHLC:', scraper.get_application_chlc())
    print('Chall CHLC:', scraper.get_challenge_chlc())
    print('Git Repo:', scraper.get_git_repo())
    exit(0)
##########################################################################


    # # Check if push is disabled
    # if test_mode:
    #     print(f'{constants.HEADER}######## TEST MODE - GIT PUSH & API CALLS ARE DISABLED{constants.ENDC}')

    # if auto_mode:
    #     print(f'{constants.HEADER}######## API Auto transitioning Jira tickets enabled{constants.ENDC}')
    # else:
    #     print(f'{constants.HEADER}######## API disabled{constants.ENDC}')

    # # Get all repository information
    # repository = clone_repository(repo_name)
    # branches = get_branches(repository)
    # is_full_app = isFullApp(repository)
    # repository_dir = get_repository_dir(repo_name)

    # Print Details about the repository
    print(f'Repo:{constants.OKCYAN} {repo_name}{constants.ENDC}')
    print(f'Branches:{constants.OKCYAN} {len(branches)}{constants.ENDC}')

    if is_full_app:
        print(f'Type: {constants.OKCYAN}Full App{constants.ENDC}')
    else:
        print(f'Type: {constants.OKCYAN}Minified App{constants.ENDC}')

    if not auto_mode:
        print(f'{constants.WARNING}\n1. Transition CHLRQ to Planned (choose this month)')
        print('2. Transition CHLRQ to In Progress')
        print(f'3. Locate the branch to make the fix on (if secure, choose secure){constants.ENDC}')

    # Continue to fix branches until user is done
    while not done_fixing:

        ###########
        #
        # Allow user to stop fixing branch at anytime
        #
        ###########

        # Fix the branch and retrieve the name and fix explanation
        fix_message, fixed_branch = fix_and_commit_branch(repository, repository_dir, branches, is_full_app, debug)

        # Remove initial_branch from branches to avoid cherry-picking it
        branches.remove(fixed_branch)

        # Add message to list of messages
        fix_messages.append(fix_message)

        # Keep track of chunks needing to be fixed
        if did_commit_add_or_remove_lines(repository):
            fix_chunks_required = True

        # If full app and fix was on the secure branch, cherry-pick branches
        if is_full_app and fixed_branch == constants.JIRA_FA_SECURE_BRANCH:

            # Get the commit ID
            commit_id = repository.rev_parse('HEAD')

            # Run cherry-pick method
            git.cherrypick(repository_dir, branches, commit_id, debug)

            # Confirm that cherrypick occurred
            did_cherrypick = True

        # Prompt user to fix another branch
        fix_branch = input(f'\nFix another branch? (y/{constants.BOLD}{constants.WHITE}N{constants.ENDC}){constants.ENDC}: {constants.WHITE}')

        print(constants.ENDC, end='')

        # If not yes, user is done fixing
        if fix_branch != 'y':
            done_fixing = True

    # If test mode, don't push to repository
    if test_mode:
        input(f'{constants.HEADER}\nPush Disabled. Press [ENTER] to continue{constants.ENDC}')
    else:
        input(f'{constants.UNDERLINE}{constants.OKGREEN}{constants.BOLD}\nPress [ENTER] to push to repo{constants.ENDC}')

        # Push commit to the repository
        subprocess.check_output(f'git -C {repository_dir} push --all', shell=True)

    # If api is enabled, transition tickets through the jira api
    if auto_mode:
        # If parameter not entered, prompt user for CHRLQ
        if not chlrq:
            chlrq = utils.get_chlrq()

        # Automatically transition jira tickets
        transition_jira_issues(chlrq, format_messages(fix_messages), did_cherrypick)
    
    # Otherwise prompt user to transition manually
    else:
        print(f'{constants.WARNING}\n1. Close CHLRQ (add the commit in as a comment){constants.WHITE}')

        # Print fix messages
        for message in fix_messages:
            print(f'\t{message}')

        print(f'{constants.ENDC}{constants.WARNING}2. Link CHLRQ to challenge CHLC (choose \'relates to\'){constants.ENDC}')

        if did_cherrypick:
            chlc = input('Enter application CHLC number [Ex: 1234]: ')

            # Open web browser to bulk transition tickets linked to the application CHLC
            webbrowser.open(f'https://securecodewarrior.atlassian.net/browse/CHLC-{chlc}?jql=project%20%3D%20%27CHLC%27%20and%20issuetype%3D%20challenge%20and%20issue%20in%20linkedIssues(%27CHLC-{chlc}%27)%20ORDER%20BY%20created%20DESC')

            print(f'\n{constants.WARNING}Follow these steps in the open tab')
            print('1. Bulk change all -> Select all -> Transition -> FEEDBACK OPEN -> confirm')
            print('2. Bulk change all -> Select all -> Transition -> FEEDBACK REVIEW -> confirm')
            print(f'3. Bulk change all -> Select all -> Edit -> Change assignee to \'Thomas Pieters\' -> add CHLRQ-#### in comment [ex: CHLRQ-1234] -> confirm{constants.ENDC}')
        
        else:
            print(f'\n{constants.WARNING}Transition the challenge CHLC')
            print('1. Transition to FEEDBACK OPEN')
            print('2. Transition to FEEDBACK REVIEW')
            print(f'3. Set assignee to \'Thomas Pieters\'')
            print(f'4. In comment, add link to CHLRQ{constants.ENDC}')

    print(f'{constants.HEADER}\nCOMPLETE THE FOLLOWING TASKS:')
    print(f'####################################')
    print('# 1. Update CMS branches to latest #')

    # Notify user to check chunks if lines were added
    if fix_chunks_required:
        print('#                                  #')
        print('# 2. Commit added or removed lines #')
        print('#    Make sure chunks are correct  #')
    
    print(f'####################################{constants.ENDC}')

    print(f'{constants.OKGREEN}{constants.BOLD}{constants.UNDERLINE}\nBug Fix Complete.{constants.ENDC}')
