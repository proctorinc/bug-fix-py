import subprocess
from git.exc import GitCommandError
import readline

from bugfix.formatting import (
    Completer,
    Colors
)

from bugfix.constants import (
    FA_SECURE_BRANCH
)

def fix_and_commit_branch(repository, repository_dir, branches, is_full_app, debug, chlrq):
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
    readline.set_completer(Completer().get_list_completer(branches))

    # Prompt user for branch where the fix will be made
    initial_branch = input(f'\nEnter branch where the fix will be made: {Colors.WHITE}')

    print(Colors.ENDC, end='')

    # Check that user input is a valid branch
    while initial_branch not in branches:

        # Alert user branch name is invalid
        print(f'{Colors.FAIL}\"{initial_branch}\" is not a valid branch name{Colors.ENDC}')

        # Check if user entered "secure" on a minified app. Suggest minified secure branch
        if (not is_full_app) and initial_branch == FA_SECURE_BRANCH:
            minified_secure_branches = getMinifiedSecureBranch(branches)
            print(f'\nThis app is {Colors.OKCYAN}Minified{Colors.ENDC}, enter the correct secure branch: {Colors.HEADER}')
            for branch in minified_secure_branches:
                print(branch, end=' ')
            print(Colors.ENDC)

        # Prompt user for branch again
        initial_branch = input(f'Enter branch where the fix will be made: {Colors.WHITE}')

        print(Colors.ENDC, end='')

    # Disable tab completion
    readline.parse_and_bind('tab: self-insert')

    # Checkout to branch
    repository.git.checkout(initial_branch)

    # Prompt user to make fix
    print(f'{Colors.UNDERLINE}{Colors.OKGREEN}{Colors.BOLD}\nMake the fix in VS Code{Colors.ENDC}')

    # Open VS Code to make fix
    subprocess.check_output(f'code {repository_dir}', shell=True)

    # Continue until fix message is entered
    while not fix_message:
        # Prompt user to input fix message
        fix_message = input(f'Enter description of fix: {Colors.WHITE}')

        print(Colors.ENDC, end='')

    # Continue until a valid commit is successful
    while not successful_commit:
        try:
            # Add files for commit
            repository.git.add(u=True)
            # subprocess.check_output(f'git -C {repository_dir} add --all', shell=True)

            # Commit
            repository.git.commit('-m', f'CHLRQ-{chlrq}: {fix_message}')
            # subprocess.check_output(f'git -C {repository_dir} commit -m \'{fix_message}\'', shell=True)

        except GitCommandError as e:
            if debug:
                print(f'{Colors.FAIL}DEBUG: error=[{e}]')
            # Alert user that no change has been made
            print(f'{Colors.ENDC}{Colors.FAIL}No Changes have been made, please make a fix before continuing')
            print(f'Press {Colors.UNDERLINE}ctrl+s{Colors.ENDC}{Colors.FAIL} to confirm changes')

            # Prompt user to press enter when fix is made
            input(f'{Colors.UNDERLINE}{Colors.OKGREEN}{Colors.BOLD}\nPress [Enter] after fix{Colors.ENDC}')

        else:
            successful_commit = True

    return fix_message, initial_branch

def getMinifiedSecureBranch(branches):
    """
    Gets the secure branch of a minified app. Minified app's secure branch starts with 'secure'
    """
    secure_branches = []

    for branch in branches:
        
        # Check if branch starts with 'secure'
        if FA_SECURE_BRANCH in branch:
            secure_branches.append(branch)

    return secure_branches