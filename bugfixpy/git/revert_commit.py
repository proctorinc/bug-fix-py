from git import GitError

from bugfixpy.utils.text import colors
from bugfixpy.exceptions import MergeConflictError
from bugfixpy.utils import prompt_user

from .repository import Repository


class RevertCommit:

    __repository: Repository
    __commit_id: str

    def __init__(self, repository, commit_id) -> None:
        self.__repository = repository
        self.__commit_id = commit_id

    def run(self) -> None:
        branches = self.__repository.get_branches()

        try:
            self.__repository.checkout_to_branch(branches[0])

        except Exception as err:
            print("Exception has occured. Exiting...\n", err)
            exit(1)

        for i, branch in enumerate(branches):
            successful_checkout = False
            try:
                self.__repository.revert_commit(self.__commit_id)

            except MergeConflictError as err:
                print("Merge conflict?", err)
            except GitError as err:
                print("Error reverting fix:", err)
                exit(1)

            while not successful_checkout:
                try:
                    self.__repository.checkout_to_branch(branches[0])
                except MergeConflictError:
                    print(
                        f"{colors.WARNING}[ !!! ]{colors.ENDC} {branch}: {colors.WARNING}MERGE CONFLICT"
                    )
                    self.__repository.open_code_in_editor()
                    prompt_user.to_resolve_merge_conflict()

                    try:
                        self.__repository.add_changes()
                        self.__repository.commit_changes_with_message(
                            f"Revert commit {self.__commit_id}"
                        )

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
