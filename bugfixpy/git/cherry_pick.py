from bugfixpy.constants import colors
from bugfixpy.exceptions import ContinueCherryPickingFailedError
from bugfixpy.utils import prompt_user
from bugfixpy.exceptions import CheckoutFailedError, MergeConflictError

from .repository import Repository


class CherryPick:

    __repository: Repository
    __commit_id: str
    __branches: list[str]

    def __init__(self, repository: Repository) -> None:
        self.__repository = repository
        self.__commit_id = repository.get_last_commit_id()
        self.__branches = self.__get_branches_without_secure()

    def across_all_branches(self) -> None:
        for i, branch in enumerate(self.__branches):
            self.__checkout_to_and_cherrypick_branch(branch)
            self.__display_percentage_complete(i)

    def __get_branches_without_secure(self) -> list[str]:
        branches = self.__repository.get_branches()
        branches.remove("secure")
        return branches

    def __checkout_to_and_cherrypick_branch(self, branch: str) -> None:
        try:
            self.__repository.checkout_to_branch(branch)
            self.__cherry_pick_branch(branch)

        except CheckoutFailedError as err:
            print(f"Exception occurred while checking out to branch: {err}")
            prompt_user.if_they_want_to_continue()

    def __cherry_pick_branch(self, branch: str) -> None:
        try:
            self.__repository.cherry_pick(self.__commit_id)

        except MergeConflictError:
            self.__alert_user_merge_conflict_occured(branch)
            self.__resolve_merge_conflict()

    def __resolve_merge_conflict(self) -> None:
        self.__repository.open_code_in_editor()
        prompt_user.to_resolve_merge_conflict()
        self.__continue_cherry_picking()

    def __continue_cherry_picking(self) -> None:
        try:
            self.__repository.add_changes()
            self.__repository.continue_cherrypicking()

        except ContinueCherryPickingFailedError:
            self.__repository.commit_changes_allow_empty()

    def __alert_user_merge_conflict_occured(self, branch: str) -> None:
        print(
            f"{colors.WARNING}[ !!! ]{colors.ENDC} {branch}: {colors.WARNING}MERGE CONFLICT"
        )

    def __display_percentage_complete(self, current_index: int) -> None:
        percentage = (current_index + 1) * 100 / len(self.__branches)
        print(
            f"[{colors.OKCYAN}{percentage:.1f}%{colors.ENDC}]{colors.ENDC}"
            f" {self.__branches[current_index]}: {colors.OKGREEN}[COMPLETE]{colors.ENDC}"
        )
