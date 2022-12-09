from git import GitError

from bugfixpy.constants import colors
from bugfixpy.exceptions import MergeConflictError
from bugfixpy.utils import prompt_user


def revert_commit_in_repository(repository, commit_id: str) -> None:
    """Reverts commit based off of commit id"""
    branches = repository.get_branches()

    try:
        repository.checkout_to_branch(branches[0])

    except Exception as err:
        print("Exception has occured. Exiting...\n", err)
        exit(1)

    # Checkout to each branch and revert commit
    for i, branch in enumerate(branches):
        successful_checkout = False
        try:
            repository.revert_commit(commit_id)

        except MergeConflictError as err:
            print("Merge conflict?", err)
        except GitError as err:
            print("Error reverting fix:", err)
            exit(1)

        while not successful_checkout:
            try:
                repository.checkout_to_branch(branches[0])
            except MergeConflictError:
                # Alert user of merge conflict
                print(
                    f"{colors.WARNING}[ !!! ]{colors.ENDC} {branch}: {colors.WARNING}MERGE CONFLICT"
                )
                repository.open_code_in_editor()
                prompt_user.to_resolve_merge_conflict()

                try:
                    repository.add_changes_to_branch()
                    repository.commit_changes_with_message(f"Revert commit {commit_id}")

                # Create empty commit if error occurs
                # TODO: figure out what exception is being thrown here
                except Exception as err:
                    print("Error adding and committing changes:\n", err)

            else:
                successful_checkout = True

        # Inform user of successful cherry-pick, branch complete
        print(
            f"[{colors.OKCYAN}{(i + 1) * 100 / len(branches):.1f}%{colors.ENDC}]{colors.ENDC}"
            f" {branch}: {colors.OKGREEN}[COMPLETE]{colors.ENDC}"
        )
