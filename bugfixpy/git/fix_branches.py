from git import GitCommandError

from bugfixpy.utils.text import colors, instructions
from bugfixpy.jira import ChallengeRequestIssue
from bugfixpy.utils import prompt_user

from .repository import Repository
from .cherry_pick import CherryPick
from .fix_result import FixResult
from . import constants


class FixBranches:

    __repository: Repository
    __challenge_request_issue: ChallengeRequestIssue
    __current_branch: str
    __fix_messages: list[str]
    __has_been_cherrypicked: bool

    def __init__(
        self,
        repository: Repository,
        challenge_request_issue: ChallengeRequestIssue,
        is_manual: bool = False,
    ) -> None:
        self.__repository = repository
        self.__challenge_request_issue = challenge_request_issue
        self.__fix_messages = []
        self.__has_been_cherrypicked = False
        self.__current_branch = self.__get_next_branch()
        self.__is_manual = is_manual

    def get_results(self) -> FixResult:
        self.run_fix()
        return self.__get_fix_result()

    def run_fix(self) -> None:
        while self.__is_another_branch_to_fix():
            self.__make_fix_in_branch()
            self.__current_branch = self.__get_next_branch_or_continue()

    def __is_another_branch_to_fix(self) -> bool:
        return self.__current_branch != ""

    def __get_next_branch(self) -> str:
        return prompt_user.for_branch_in_repository(self.__repository)

    def __get_next_branch_or_continue(self) -> str:
        return prompt_user.for_next_branch_or_to_continue(self.__repository)

    def __make_fix_in_branch(self) -> None:
        try:
            self.__fix_and_cherry_pick_if_required()
        except KeyboardInterrupt:
            self.__display_aborted_branch_fix()

    def __get_fix_result(self) -> FixResult:
        return FixResult(
            fix_messages=self.__fix_messages,
            repo_was_cherrypicked=self.__has_been_cherrypicked,
            is_chunk_fixing_required=self.__is_manual,
        )

    def __fix_and_cherry_pick_if_required(self) -> None:
        self.__make_change_and_commit()

        if self.__is_cherry_pick_is_required():
            self.__cherry_pick_repository()

    def __make_change_and_commit(self) -> None:
        self.__repository.checkout_to_branch(self.__current_branch)
        print(instructions.PROMPT_USER_TO_MAKE_FIX)
        self.__repository.open_code_in_editor()
        fix_message = prompt_user.for_descripton_of_fix()
        self.__attempt_to_commit_until_successful(fix_message)

    def __cherry_pick_repository(self) -> None:
        self.display_cherry_pick_to_user()
        CherryPick(self.__repository, is_manual=self.__is_manual).across_all_branches()

    def display_cherry_pick_to_user(self) -> None:
        input("Cherry picking required. Press [ENTER] to start")

    def __is_cherry_pick_is_required(self) -> bool:
        return (
            self.__repository.is_full_app()
            and self.__current_branch == constants.FULL_APP_SECURE_BRANCH
        )

    def __attempt_to_commit_until_successful(self, fix_message: str) -> None:
        successful_commit = False

        while not successful_commit:
            try:
                successful_commit = self.__commit_changes(fix_message)

            except GitCommandError:
                self.__get_user_to_make_changes()

    def __commit_changes(self, fix_message: str) -> bool:
        self.__repository.add_changes()
        message = self.__add_challenge_request_id_to_message(fix_message)
        self.__repository.commit_changes_with_message(message)
        self.__fix_messages.append(fix_message)

        return True

    def __add_challenge_request_id_to_message(self, fix_message: str) -> str:
        message = self.__challenge_request_issue.get_issue_id() + ": " + fix_message
        return str(message)

    def __get_user_to_make_changes(self) -> None:
        print(instructions.PROMPT_USER_THAT_NO_FIX_WAS_MADE)
        prompt_user.to_press_enter()

    def __display_aborted_branch_fix(self) -> None:
        print(
            f'\n{colors.FAIL}Fixing branch "{self.__current_branch}" aborted.{colors.ENDC}'
        )
