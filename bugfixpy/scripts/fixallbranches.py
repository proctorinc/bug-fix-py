# TODO: put this in main? Or in new script file
from ..gitrepository import GitRepository
from .fixbranch import fix_and_commit_branch
from ..constants import jira, colors


def fix_branches_in_repository(repository: GitRepository) -> None:
    """
    Run bug fix. Loop over branches to fix. After fixing, prompt
    user if they want to fix another
    """
    branches = repository.get_filtered_branches()
    is_full_app = repository.is_full_app()

    # Default user is not done fixing branches
    done_fixing = False

    # Hold fix messages for all branches in list
    fix_messages = []

    # Continue to fix branches until user is done
    while not done_fixing:

        ###########
        #
        # Allow user to stop fixing branch at anytime
        #
        ###########

        # Fix the branch and retrieve the name and fix explanation
        fix_message, fixed_branch = fix_and_commit_branch(repository)

        # Remove initial_branch from branches to avoid cherry-picking it
        branches.remove(fixed_branch)

        # Add message to list of messages
        fix_messages.append(fix_message)

        # If full app and fix was on the secure branch, cherry-pick branches
        if is_full_app and fixed_branch == jira.FULL_APP_SECURE_BRANCH:

            # Get the commit ID
            commit_id = repository.get_last_commit_id()

            print("\nCherry-picking Branches...")
            # Run cherry-pick method
            repository.cherrypick_commit_across_all_branches(commit_id)

            # Confirm that cherrypick occurred
            repository.set_cherrypick_ran()

        # Prompt user to fix another branch
        fix_branch = input(
            f"\nFix another branch? (y/{colors.BOLD}{colors.WHITE}N{colors.ENDC}){colors.ENDC}: {colors.WHITE}"
        )

        print(colors.ENDC, end="")

        # If not yes, user is done fixing
        if fix_branch != "y":
            done_fixing = True
