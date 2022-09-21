import subprocess
import webbrowser
from bugfix.utils import (
    cherry_pick,
    is_valid_chlrq,
    is_valid_chlc,
    getCHLRQ,
    setupCredentials,
    clone_repository,
    get_branches,
    isFullApp,
    parse_arguments,
    get_repository_dir,
    fix_and_commit_branch,
    format_messages,
    did_commit_add_or_remove_lines,
    transition_jira_issues,
)
from bugfix.formatting import (
    Colors,
)
from bugfix.api import (
    has_valid_credentials,
)
from bugfix.constants import (
    API_EMAIL,
    API_KEY,
    FA_SECURE_BRANCH
)

# Main function runs bug-fix program
def main():

    # Parse commandline arguments
    args = parse_arguments()

    # Default user is not done fixing branches
    done_fixing = False

    # Set default cherrypick has not occurred
    did_cherrypick = False

    # Hold fix messages for all branches in list
    fix_messages = []

    # Track whether chunks need to be fixed or not
    fix_chunks_required = False

    # define variables from arguments
    repo_name = args.repository
    test_mode = args.test
    setup_mode = args.setup
    chlrq = args.chlrq
    chlc = args.chlc
    no_pick = args.no_pick
    only_transition_mode = args.transition
    is_api_enabled = args.api
    debug = args.debug
    
    # If setup mode is on, run setup
    if setup_mode:
        setupCredentials()

    elif only_transition_mode:

        # If parameter not entered, prompt user for CHRLQ
        if not chlrq:
            chlrq = getCHLRQ()

        # If parameter not entered, prompt user for CHLC
        # if not chlc:
        #     chlc = get_chlc()

        # Ask user if bulk transition is required
        if input(f'Is bulk transition required? ({Colors.BOLD}{Colors.WHITE}Y{Colors.ENDC}/n): {Colors.WHITE}') != 'n':
            did_cherrypick = True

        fix_messages = input(f'{Colors.ENDC}Enter fix message: {Colors.WHITE}')

        print(Colors.ENDC)

        # Automatically transition jira tickets
        transition_jira_issues(chlrq, fix_messages, did_cherrypick)

        exit(0)

    # Check if environment variables do not exist
    elif (not test_mode) and is_api_enabled and (not API_EMAIL or not API_KEY):
        print(f'{Colors.FAIL}Credentials not setup. Run \'bug-fix.py --setup\' to set up environment variables{Colors.ENDC}')

        # Notify that no email is present
        if not API_EMAIL:
            print(f'{Colors.FAIL}No API email present{Colors.ENDC}')

        # Notify that no api key is present
        if not API_KEY:
            print(f'{Colors.FAIL}No API key present{Colors.ENDC}')

        exit(1)

    # Check if API credentials are valid, otherwise exit program
    if not test_mode and is_api_enabled and not has_valid_credentials():
        print(f'{Colors.FAIL}Invalid API credentials. Run with --setup to change credentials{Colors.ENDC}')
        exit(1)

    # Only get ticket numbers if API is enabled
    if is_api_enabled:

        # Check that CHLRQ is valid
        if chlrq and not is_valid_chlrq(chlrq):
            # Alert user chlrq is invalid
            print(f'{Colors.FAIL}CHLRQ-{chlrq} is not valid.{Colors.ENDC}')
            exit(1)

        # Check that CHLC is valid
        if chlc and not is_valid_chlc(chlc):
            # Alert user chlrq is invalid
            print(f'{Colors.FAIL}CHLC-{chlc} is not valid.{Colors.ENDC}')
            exit(1)

    # Check if push is disabled
    if test_mode:
        print(f'{Colors.HEADER}######## TEST MODE - GIT PUSH & API CALLS ARE DISABLED{Colors.ENDC}')

    if no_pick:
        print(f'{Colors.HEADER}######## Cherry-pick disabled - will not cherry-pick all branches{Colors.ENDC}')

    if is_api_enabled:
        print(f'{Colors.HEADER}######## API Auto transitioning Jira tickets enabled{Colors.ENDC}')
    else:
        print(f'{Colors.HEADER}######## API disabled{Colors.ENDC}')

    # Get all repository information
    repository = clone_repository(repo_name)
    branches = get_branches(repository)
    is_full_app = isFullApp(repository)
    repository_dir = get_repository_dir(repo_name)

    # Print Details about the repository
    print(f'Repo:{Colors.OKCYAN} {repo_name}{Colors.ENDC}')
    print(f'Branches:{Colors.OKCYAN} {len(branches)}{Colors.ENDC}')

    if is_full_app:
        print(f'Type: {Colors.OKCYAN}Full App{Colors.ENDC}')
    else:
        print(f'Type: {Colors.OKCYAN}Minified App{Colors.ENDC}')

    # If parameter not entered, prompt user for CHRLQ
    if not chlrq:
        chlrq = getCHLRQ()

    if not is_api_enabled:
        print(f'{Colors.WARNING}\n1. Transition CHLRQ to Planned (choose this month)')
        print('2. Transition CHLRQ to In Progress')
        print(f'3. Locate the branch to make the fix on (if secure, choose secure){Colors.ENDC}')

    # Continue to fix branches until user is done
    while not done_fixing:

        # Fix the branch and retrieve the name and fix explanation
        fix_message, fixed_branch = fix_and_commit_branch(repository, repository_dir, branches, is_full_app, debug, chlrq)

        # Remove initial_branch from branches to avoid cherry-picking it
        branches.remove(fixed_branch)

        # Add message to list of messages
        fix_messages.append(fix_message)

        # Keep track of chunks needing to be fixed
        if did_commit_add_or_remove_lines(repository):
            fix_chunks_required = True

        # If full app and fix was on the secure branch, cherry-pick branches
        if is_full_app and fixed_branch == FA_SECURE_BRANCH:

            # Get the commit ID
            commit_id = repository.rev_parse('HEAD')

            # If cherry pick is not disabled
            if not no_pick:

                # Run cherry-pick method
                cherry_pick(repository_dir, branches, commit_id, debug)

            # Confirm that cherrypick occurred
            did_cherrypick = True

        # Prompt user to fix another branch
        fix_branch = input(f'\nFix another branch? (y/{Colors.BOLD}{Colors.WHITE}N{Colors.ENDC}){Colors.ENDC}: {Colors.WHITE}')

        print(Colors.ENDC, end='')

        # If not yes, user is done fixing
        if fix_branch != 'y':
            done_fixing = True

    # If test mode, don't push to repository
    if test_mode:
        input(f'{Colors.HEADER}\nPush Disabled. Press [ENTER] to continue{Colors.ENDC}')
    else:
        input(f'{Colors.UNDERLINE}{Colors.OKGREEN}{Colors.BOLD}\nPress [ENTER] to push to repo{Colors.ENDC}')

        # Push commit to the repository
        subprocess.check_output(f'git -C {repository_dir} push --all', shell=True)

    # If api is enabled, transition tickets through the jira api
    if is_api_enabled:
        ###############################################
        # CHLC no longer required. Linking not needed #
        ###############################################
        # # If parameter not entered, prompt user for CHLC
        # if not chlc:
        #     chlc = get_chlc()

        # Automatically transition jira tickets
        transition_jira_issues(chlrq, format_messages(fix_messages), did_cherrypick)
    
    # Otherwise prompt user to transition manually
    else:
        print(f'{Colors.WARNING}\n1. Close CHLRQ (add the commit in as a comment){Colors.WHITE}')

        # Print fix messages
        for message in fix_messages:
            print(f'\t{message}')

        print(f'{Colors.ENDC}{Colors.WARNING}2. Link CHLRQ to challenge CHLC (choose \'relates to\'){Colors.ENDC}')

        if did_cherrypick:
            chlc = input('Enter application CHLC number [Ex: 1234]: ')

            # Open web browser to bulk transition tickets linked to the application CHLC
            webbrowser.open(f'https://securecodewarrior.atlassian.net/browse/CHLC-{chlc}?jql=project%20%3D%20%27CHLC%27%20and%20issuetype%3D%20challenge%20and%20issue%20in%20linkedIssues(%27CHLC-{chlc}%27)%20ORDER%20BY%20created%20DESC')

            print(f'\n{Colors.WARNING}Follow these steps in the open tab')
            print('1. Bulk change all -> Select all -> Transition -> FEEDBACK OPEN -> confirm')
            print('2. Bulk change all -> Select all -> Transition -> FEEDBACK REVIEW -> confirm')
            print(f'3. Bulk change all -> Select all -> Edit -> Change assignee to \'Thomas Pieters\' -> add CHLRQ-#### in comment [ex: CHLRQ-1234] -> confirm{Colors.ENDC}')
        
        else:
            print(f'\n{Colors.WARNING}Transition the challenge CHLC')
            print('1. Transition to FEEDBACK OPEN')
            print('2. Transition to FEEDBACK REVIEW')
            print(f'3. Set assignee to \'Thomas Pieters\'')
            print(f'4. In comment, add link to CHLRQ{Colors.ENDC}')

    print(f'{Colors.HEADER}\nCOMPLETE THE FOLLOWING TASKS:')
    print(f'####################################')
    print('# 1. Update CMS branches to latest #')

    # Notify user to check chunks if lines were added
    if fix_chunks_required:
        print('#                                  #')
        print('# 2. Commit added or removed lines #')
        print('#    Make sure chunks are correct  #')
    
    print(f'####################################{Colors.ENDC}')

    print(f'{Colors.OKGREEN}{Colors.BOLD}{Colors.UNDERLINE}\nBug Fix Complete.{Colors.ENDC}')
