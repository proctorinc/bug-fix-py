import subprocess
import git
import readline
from src import utils
from src import constants
from src.constants import colors

def filter_branches(remote_refs): # only used here
    """
    Parse branches from remote refs and remove unwanted branches
    """
    filtered_branches = []

    # Loop over remote references
    for refs in remote_refs:

        # Remove origin/ from branch name
        branch = refs.name.split("origin/",1)[1]

        # Filter branches
        if branch not in constants.JIRA_IGNORE_BRANCHES:
            filtered_branches.append(branch)

    return filtered_branches

def retrieve_branches(repository): # used in bugfix main
    """
    Gets branches from a github repository. Filters out unwanted branches
    """
    # Get all branches
    return filter_branches(repository.remote().refs)

#
# Need a better implementation of this using the scraper. This method is not reliable
#

def check_is_full_app(branches): # used in bugfix main
    """
    Returns true if repository is a full app, false if it is minified.
    Full app determined if branches contain "secure" branch
    """
    is_full_app = False

    # If full app branch exists, repo is a full app, otherwise it is minified
    if constants.JIRA_FA_SECURE_BRANCH in branches:
        is_full_app = True
    
    return is_full_app

def cherrypick(repository_dir, branches, commit_id):

    print(f'\nCherry-picking Branches...')

    # Execute command in each branch
    for i, branch in enumerate(branches):

        # Checkout to branch
        checkout_result = subprocess.check_output(f'git -C {repository_dir} checkout {branch} &>/dev/null',
                                        shell=True)

        if 'error' in checkout_result.decode('utf-8') or 'fatal' in checkout_result.decode('utf-8'):
            print('ERROR: Checkout failed')
            print(checkout_result.decode('utf-8'))

            print('\nAn error may have occured. Review the above message and determine if you should exit or continue.')
            exit_program = input('Would you like to exit? (Y/n): ')

            if exit_program.upper() == 'N':
                print('Continuing..')
            else:
                exit(1)

        # Successful checkout to branch
        else:
            # Cherry-pick branch
            cherrypick_result = subprocess.check_output(f'git -C {repository_dir} cherry-pick {commit_id} &>/dev/null', shell=True)

            # if debug:
            #     print(f'{colors.FAIL}DEBUG: result=[', cherrypick_result.decode('utf-8'), ']')
            if not cherrypick_result.decode('utf-8') or 'Auto-merging' in cherrypick_result.decode('utf-8'):

                # Alert user of merge conflict
                print(f'{colors.WARNING}[ !!! ]{colors.ENDC} {branch}: {colors.WARNING}MERGE CONFLICT')

                # Open VS Code to solve merge conflict
                subprocess.check_output(f'code {repository_dir}', shell=True)

                input(f'\n{colors.ENDC}{colors.BOLD}Press {colors.OKGREEN}[ENTER] {colors.ENDC}{colors.BOLD}when changes have been made{colors.ENDC}')

                try:
                    subprocess.call(f'git -C {repository_dir} add .',
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
                    subprocess.call(f'git -C {repository_dir} cherry-pick --continue',
                        shell=True)

                except:
                    # print('Caught exception!')
                    subprocess.call(f'git -C {repository_dir} commit --allow-empty',
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)

        # Inform user of successful cherry-pick, branch complete
        print(f'[{colors.OKCYAN}{(i + 1) * 100 / len(branches):.1f}%{colors.ENDC}]{colors.ENDC} {branch}: {colors.OKGREEN}[COMPLETE]{colors.ENDC}')

def fix_and_commit_branch(repository, repository_dir, branches, is_full_app):
    """
    Checks the user out to a branch of their choice, making sure it is a valid branch.
    Opens VS Code for user to make the fix and prompts user to press ENTER when done.
    Continues process if changes were made successfully and commits with a message.
    Returns the commit message and the branch the user successfully fixed.
    """
    # Default commit to unsuccessful
    successful_commit = False

    # Default fix message to blank
    fix_message = ''

    # Enable tab completion
    readline.parse_and_bind("tab: complete")
    
    # Set completion to list of branches
    readline.set_completer(utils.Completer().get_list_completer(branches))

    # Prompt user for branch where the fix will be made
    initial_branch = input(f'\nEnter name of branch to fix: {colors.WHITE}')

    print(colors.ENDC, end='')

    # Check that user input is a valid branch
    while initial_branch not in branches:

        # Alert user branch name is invalid
        print(f'{colors.FAIL}\"{initial_branch}\" is not a valid branch name{colors.ENDC}')

        # Check if user entered "secure" on a minified app. Suggest minified secure branch
        if (not is_full_app) and initial_branch == constants.JIRA_FA_SECURE_BRANCH:
            minified_secure_branches = get_minified_secure_branch(branches)
            print(f'\nThis app is {colors.OKCYAN}Minified{colors.ENDC}, enter the correct secure branch: {colors.HEADER}')
            for branch in minified_secure_branches:
                print(branch, end=' ')
            print(colors.ENDC)

        # Prompt user for branch again
        initial_branch = input(f'Enter name of branch to fix: {colors.WHITE}')

        print(colors.ENDC, end='')

    # Disable tab completion
    readline.parse_and_bind('tab: self-insert')

    # Checkout to branch
    repository.git.checkout(initial_branch)

    # Prompt user to make fix
    print(f'{colors.UNDERLINE}{colors.OKGREEN}{colors.BOLD}\nMake the fix in VS Code{colors.ENDC}')

    # Open VS Code to make fix
    subprocess.check_output(f'code {repository_dir}', shell=True)

    # Continue until fix message is entered
    while not fix_message:
        # Prompt user to input fix message
        fix_message = input(f'Enter description of fix: {colors.WHITE}')

        print(colors.ENDC, end='')

    # Continue until a valid commit is successful
    while not successful_commit:
        try:
            # Add files for commit
            repository.git.add(u=True)
            # subprocess.check_output(f'git -C {repository_dir} add --all', shell=True)

            # Commit
            repository.git.commit('-m', fix_message)
            # subprocess.check_output(f'git -C {repository_dir} commit -m \'{fix_message}\'', shell=True)

        except git.exc.GitCommandError as e:
            # if debug:
            #     print(f'{colors.FAIL}DEBUG: error=[{e}]')
            # Alert user that no change has been made
            print(f'{colors.ENDC}{colors.FAIL}No Changes have been made, please make a fix before continuing')
            print(f'Press {colors.UNDERLINE}ctrl+s{colors.ENDC}{colors.FAIL} to confirm changes')

            # Prompt user to press enter when fix is made
            input(f'{colors.UNDERLINE}{colors.OKGREEN}{colors.BOLD}\nPress [Enter] after fix{colors.ENDC}')

        else:
            successful_commit = True

    return fix_message, initial_branch

def get_minified_secure_branch(branches):
    """
    Gets the secure branch of a minified app. Minified app's secure branch starts with 'secure'
    """
    secure_branches = []

    for branch in branches:
        
        # Check if branch starts with 'secure'
        if constants.JIRA_FA_SECURE_BRANCH in branch:
            secure_branches.append(branch)

    return secure_branches