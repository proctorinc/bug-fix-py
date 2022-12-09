from bugfixpy.constants import colors
from bugfixpy.exceptions import ContinueCherryPickingFailedError
from bugfixpy.utils import prompt_user
from bugfixpy.exceptions import CheckoutFailedError, MergeConflictError

from .repository import Repository


class CherryPick:

    repository: Repository
    branches: list[str]
    commit_id: str

    def __init__(self, repository, commit_id) -> None:
        self.repository = repository
        self.branches = repository.get_branches()
        self.commit_id = commit_id

    def across_all_branches(self) -> None:
        for i, branch in enumerate(self.branches):
            self.__checkout_to_and_cherrypick_branch(branch)
            self.__display_percentage_complete(i)

    def __checkout_to_and_cherrypick_branch(self, branch) -> None:
        try:
            self.repository.checkout_to_branch(branch)
            self.__cherry_pick_branch(branch)

        except CheckoutFailedError as err:
            print("Exception occurred while checking out to branch")
            print(err)
            prompt_user.if_they_want_to_continue()

    def __cherry_pick_branch(self, branch) -> None:
        try:
            self.repository.cherry_pick(self.commit_id)

        except MergeConflictError as err:
            print(err)
            self.__alert_user_merge_conflict_occured(branch)
            self.__resolve_merge_conflict()

    def __resolve_merge_conflict(self) -> None:
        self.repository.open_code_in_editor()
        prompt_user.to_resolve_merge_conflict()
        self.__continue_cherry_picking()

    def __continue_cherry_picking(self) -> None:
        try:
            self.repository.add_changes()
            self.repository.continue_cherrypicking()

        except ContinueCherryPickingFailedError:
            self.repository.commit_changes_allow_empty()

    def __alert_user_merge_conflict_occured(self, branch) -> None:
        print(
            f"{colors.WARNING}[ !!! ]{colors.ENDC} {branch}: {colors.WARNING}MERGE CONFLICT"
        )

    def __display_percentage_complete(self, current_index) -> None:
        percentage = (current_index + 1) * 100 / len(self.branches)
        print(
            f"[{colors.OKCYAN}{percentage:.1f}%{colors.ENDC}]{colors.ENDC}"
            f" {self.branches[current_index]}: {colors.OKGREEN}[COMPLETE]{colors.ENDC}"
        )
