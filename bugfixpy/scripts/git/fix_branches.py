"""
Fix Branches script fixes and commits changes to branches until the user is done fixing
"""

from git import GitCommandError
from bugfixpy.git.gitrepository import GitRepository
from bugfixpy.constants import jira, colors, instructions
from bugfixpy.utils import user_input
from bugfixpy.scripts.git import cherrypick_commit_across_all_branches


def fix_branches_in_repository(repository: GitRepository) -> None:
    """
    Run bug fix. Loop over branches to fix. After fixing, prompt
    user if they want to fix another
    """
    branches = repository.get_filtered_branches()

    # Default user is not done fixing branches
    done_fixing = False

    # Hold fix messages for all branches in list
    fix_messages = []

    # Continue to fix branches until user is done
    while not done_fixing:

        # Get next branch to fix
        current_branch = user_input.get_next_branch(branches, repository)

        # Allow the user to use a keyboard interrupt to stop fixing a branch at anytime
        try:
            # Fix the branch and retrieve the name and fix explanation
            fix_message = __make_fix_and_commit(current_branch, repository)

            # Add message to list of messages
            fix_messages.append(fix_message)

            # If full app and fix was on the secure branch, cherry-pick branches
            if (
                repository.is_full_app()
                and current_branch == jira.FULL_APP_SECURE_BRANCH
            ):

                # Get the commit ID
                commit_id = repository.get_last_commit_id()

                print("\nCherry-picking Branches...")
                # Run cherry-pick method
                cherrypick_commit_across_all_branches(repository, commit_id)

                # Confirm that cherrypick occurred
                repository.set_cherrypick_ran()

        # Catch keyboard interrupt to cancel fixing the current branch
        except KeyboardInterrupt:
            print(f'\n{colors.FAIL}Fixing branch "{current_branch}" aborted.')

        # Prompt user if they want to fix another branch
        done_fixing = user_input.prompt_want_to_continue()

        print(colors.ENDC, end="")


# TODO: implement fixing all branches option
# # VERSION TO FIX ALL BRANCHES AT ONCE
# def fix_branches_in_repository(repository: GitRepository) -> None:
#     """
#     Run bug fix. Loop over branches to fix. After fixing, prompt
#     user if they want to fix another
#     """
#     branches = repository.get_filtered_branches()

#     # Hold fix messages for all branches in list
#     fix_messages = []

#     print("Fixing all branches in the repository...")

#     # Continue to fix branches until user is done
#     while branches:

#         # Get next branch to fix
#         current_branch = branches.pop()

#         # Allow the user to use a keyboard interrupt to stop fixing a branch at anytime
#         try:
#             # Fix the branch and retrieve the name and fix explanation
#             fix_message = __make_fix_and_commit(current_branch, repository)

#             # Add message to list of messages
#             fix_messages.append(fix_message)

#             # If full app and fix was on the secure branch, cherry-pick branches
#             if (
#                 repository.is_full_app()
#                 and current_branch == jira.FULL_APP_SECURE_BRANCH
#             ):

#                 confirm_cherrypick = input("Would you like to cherrypick this branch? (Y/n): ")

#                 if confirm_cherrypick in ["n", "N"]:
#                     break

#                 # Get the commit ID
#                 commit_id = repository.get_last_commit_id()

#                 print("\nCherry-picking Branches...")
#                 # Run cherry-pick method
#                 cherrypick_commit_across_all_branches(repository, commit_id)

#                 # Confirm that cherrypick occurred
#                 repository.set_cherrypick_ran()

#         # Catch keyboard interrupt to cancel fixing the current branch
#         except KeyboardInterrupt:
#             print(f'\n{colors.FAIL}Fixing branch "{current_branch}" aborted.')

#         print(colors.ENDC, end="")


def __make_fix_and_commit(branch: str, repository: GitRepository) -> str:
    """
    Checks the user out to a branch of their choice, making sure it is a valid branch.
    Opens VS Code for user to make the fix and prompts user to press ENTER when done.
    Continues process if changes were made successfully and commits with a message.
    Returns the commit message and the branch the user successfully fixed.
    """

    # Default commit to unsuccessful
    successful_commit = False

    # Checkout to branch
    repository.checkout_to_branch(branch)

    # Prompt user to make fix
    print(instructions.PROMPT_USER_TO_MAKE_FIX)

    # Open VS Code to make fix
    repository.open_code_in_editor()

    # Prompt for user to enter commit message
    fix_message = user_input.get_fix_message()

    # Continue until a valid commit is successful
    while not successful_commit:
        try:
            # Add files for commit
            repository.add_changes_to_branch()

            # Commit changes in branch with message
            repository.commit_changes_with_message(fix_message)

        except GitCommandError as err:
            print(err)
            print(instructions.PROMPT_USER_THAT_NO_FIX_WAS_MADE)

            # Prompt user to press enter when fix is made
            user_input.prompt_user_to_press_enter()

        else:
            successful_commit = True

    return fix_message
