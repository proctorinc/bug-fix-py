"""
Cherrypick script takes a commit id and runs git cherry-pick on all branches in the repository
"""

from bugfixpy.exceptions import CheckoutFailedError, MergeConflictError
from bugfixpy.utils import user_input
from bugfixpy.gitrepository import GitRepository
from bugfixpy.constants import colors


def cherrypick_commit_across_all_branches(repository: GitRepository, commit_id) -> None:
    """
    Cherrypick git repository
    """
    branches = repository.get_filtered_branches()

    # Cherrypick each branch
    for i, branch in enumerate(branches):

        # Attempt to checkout to branch
        try:
            repository.checkout_to_branch(branch)

        # If checkout failed
        except CheckoutFailedError as err:
            print("Exception occurred while checking out to branch")
            print(err)
            user_input.prompt_user_to_exit_or_continue()

        # Successful checkout to branch
        else:
            # Attempt to cherrypick branch
            try:
                repository.cherrypick_branch(commit_id)

            # Check if merge conflict occurred
            except MergeConflictError:
                # print(instructions.WARN_USER_OF_MERGE_CONFLICT.format(branch=branch))
                print(f"{colors.WARNING}[ !!! ]{colors.ENDC} {branch}: {colors.WARNING}MERGE CONFLICT")
                repository.open_code_in_editor()
                user_input.prompt_user_to_resolve_merge_conflict()

                # Attempt to add changes and continue cherrypick
                try:
                    repository.add_changes_to_branch()
                    repository.continue_cherrypicking_branch()

                # Create empty commit if error occurs
                # TODO: figure out what exception is being thrown here
                except Exception as err:
                    print("Exception occurred while adding and continuing cherrypick")
                    print(err)
                    print(type(err))
                    repository.commit_changes_allow_empty()

        # Inform user of successful cherry-pick, branch complete
        print(
            f"[{colors.OKCYAN}{(i + 1) * 100 / len(branches):.1f}%{colors.ENDC}]{colors.ENDC}"
            f" {branch}: {colors.OKGREEN}[COMPLETE]{colors.ENDC}"
        )
