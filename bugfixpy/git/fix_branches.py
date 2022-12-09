from git import GitCommandError

from bugfixpy.constants import instructions, jira
from bugfixpy.constants import colors
from bugfixpy.jira import ChallengeRequestIssue
from bugfixpy.utils import prompt_user

from .repository import Repository
from .cherry_pick import CherryPick
from .fix_result import FixResult


class FixBranches:

    repository: Repository
    challenge_request_issue: ChallengeRequestIssue
    current_branch: str
    fix_messages: list[str]
    has_been_cherrypicked: bool

    def __init__(
        self, repository: Repository, challenge_request_issue: ChallengeRequestIssue
    ) -> None:
        self.repository = repository
        self.challenge_request_issue = challenge_request_issue
        self.fix_messages = []
        self.has_been_cherrypicked = False
        self.current_branch = self.__get_next_branch()

    def get_results(self) -> FixResult:
        self.__run_fix()
        return self.__get_fix_result()

    def __run_fix(self) -> None:
        while self.__is_another_branch_to_fix():
            self.__make_fix_in_branch()
            self.current_branch = self.__get_next_branch_or_continue()

    def __is_another_branch_to_fix(self) -> bool:
        return self.current_branch != ""

    def __get_next_branch(self) -> str:
        return prompt_user.for_branch_in_repository(self.repository)

    def __get_next_branch_or_continue(self) -> str:
        return prompt_user.for_next_branch_or_to_continue(self.repository)

    def __make_fix_in_branch(self) -> None:
        try:
            self.__fix_and_cherry_pick_if_required()

        except KeyboardInterrupt:
            self.__display_aborted_branch_fix()

    def __get_fix_result(self) -> FixResult:
        return FixResult(
            fix_messages=self.fix_messages,
            repo_was_cherrypicked=self.has_been_cherrypicked,
            is_chunk_fixing_required=True,
        )

    def __fix_and_cherry_pick_if_required(self) -> None:
        self.__make_change_and_commit()

        if self.__is_cherry_pick_is_required():
            self.__cherry_pick_repository()

    def __make_change_and_commit(self) -> None:
        self.repository.checkout_to_branch(self.current_branch)
        print(instructions.PROMPT_USER_TO_MAKE_FIX)
        self.repository.open_code_in_editor()
        fix_message = prompt_user.for_descripton_of_fix()

        self.__attempt_to_commit_until_successful(fix_message)

    def __cherry_pick_repository(self) -> None:
        commit_id = self.repository.get_last_commit_id()
        print("Cherry picking commit...")
        CherryPick(self.repository, commit_id).across_all_branches()

    def __is_cherry_pick_is_required(self) -> bool:
        return (
            self.repository.is_full_app()
            and self.current_branch == jira.FULL_APP_SECURE_BRANCH
        )

    def __attempt_to_commit_until_successful(self, fix_message: str) -> None:
        successful_commit = False

        while not successful_commit:
            try:
                successful_commit = self.__commit_changes(fix_message)

            except GitCommandError:
                self.__get_user_to_make_changes()

    def __commit_changes(self, fix_message: str) -> bool:
        self.repository.add_changes()
        message = self.__add_challenge_request_id_to_message(fix_message)
        self.repository.commit_changes_with_message(message)
        self.fix_messages.append(fix_message)

        return True

    def __add_challenge_request_id_to_message(self, fix_message: str) -> str:
        return str(self.challenge_request_issue.get_issue_id() + ": " + fix_message)

    def __get_user_to_make_changes(self) -> None:
        print(instructions.PROMPT_USER_THAT_NO_FIX_WAS_MADE)
        prompt_user.to_press_enter()

    def __display_aborted_branch_fix(self) -> None:
        print(
            f'\n{colors.FAIL}Fixing branch "{self.current_branch}" aborted.{colors.ENDC}'
        )
