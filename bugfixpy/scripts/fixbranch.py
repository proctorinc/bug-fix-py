from typing import Tuple
import readline
from git import GitCommandError

from bugfixpy.gitrepository import GitRepository
from bugfixpy.constants import colors, jira
from bugfixpy.formatting import Completer


def fix_and_commit_branch(repository: GitRepository) -> Tuple[str, str]:
    """
    Checks the user out to a branch of their choice, making sure it is a valid branch.
    Opens VS Code for user to make the fix and prompts user to press ENTER when done.
    Continues process if changes were made successfully and commits with a message.
    Returns the commit message and the branch the user successfully fixed.
    """
    branches = repository.get_filtered_branches()

    is_full_app = repository.is_full_app()

    # Default commit to unsuccessful
    successful_commit = False

    # Default fix message to blank
    fix_message = ""

    # Enable tab completion
    readline.parse_and_bind("tab: complete")

    # Set completion to list of branches
    readline.set_completer(Completer().get_list_completer(branches))

    # Prompt user for branch where the fix will be made
    initial_branch = input(f"\nEnter name of branch to fix: {colors.WHITE}")

    print(colors.ENDC, end="")

    # Check that user input is a valid branch
    while initial_branch not in branches:

        # Alert user branch name is invalid
        print(
            f'{colors.FAIL}"{initial_branch}" is not a valid branch name{colors.ENDC}'
        )

        # Check if user entered "secure" on a minified app. Suggest minified secure branch
        if (not is_full_app) and initial_branch == jira.FULL_APP_SECURE_BRANCH:
            minified_secure_branches = repository.get_minified_secure_branch()
            print(
                f"\nThis app is {colors.OKCYAN}Minified{colors.ENDC}, enter the correct secure branch: {colors.HEADER}"
            )
            for branch in minified_secure_branches:
                print(branch, end=" ")
            print(colors.ENDC)

        # Prompt user for branch again
        initial_branch = input(f"Enter name of branch to fix: {colors.WHITE}")

        print(colors.ENDC, end="")

    # Disable tab completion
    readline.parse_and_bind("tab: repository-insert")

    # Checkout to branch
    # repository.git.checkout(initial_branch)
    repository.checkout_to_branch(initial_branch)

    # Prompt user to make fix
    print(
        f"{colors.UNDERLINE}{colors.OKGREEN}{colors.BOLD}\nMake the fix in VS Code{colors.ENDC}"
    )

    # Open VS Code to make fix
    # subprocess.check_output(f"code {repository_dir}", shell=True)
    repository.open_repository_in_vscode()

    # Continue until fix message is entered
    while not fix_message:
        # Prompt user to input fix message
        fix_message = input(f"Enter description of fix: {colors.WHITE}")

        print(colors.ENDC, end="")

    # Continue until a valid commit is successful
    while not successful_commit:
        try:
            # Add files for commit
            # repository.git.add(u=True)
            repository.add_changes_to_branch()

            # Commit changes in branch with message
            repository.commit_changes_with_message(fix_message)

        except GitCommandError:
            # if debug:
            #     print(f'{colors.FAIL}DEBUG: error=[{e}]')
            # Alert user that no change has been made
            print(
                f"{colors.ENDC}{colors.FAIL}No Changes have been made, please make a fix before continuing"
            )
            print(
                f"Press {colors.UNDERLINE}ctrl+s{colors.ENDC}{colors.FAIL} to confirm changes"
            )

            # Prompt user to press enter when fix is made
            input(
                f"{colors.UNDERLINE}{colors.OKGREEN}{colors.BOLD}\nPress [Enter] after fix{colors.ENDC}"
            )

        else:
            successful_commit = True

    return fix_message, initial_branch
