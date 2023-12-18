from git import GitCommandError

from bugfixpy.jira import ChallengeRequestIssue
from bugfixpy.utils import prompt_user
from bugfixpy.utils.text import instructions

from .repository import Repository
from .cherry_pick import CherryPick
from .fix_result import FixResult


class RepoFixer:
    repository: Repository
    challenge_request_issue: ChallengeRequestIssue

    def __init__(self, repository: Repository) -> None:
        self.repository = repository

    def fix_branch_and_cherry_pick(
        self,
        branch_to_fix: str,
        cherry_pick_branches: list[str],
        challenge_request_issue: ChallengeRequestIssue,
    ) -> FixResult:
        fix_message = "Fixed vulnerable packages per dependabot alerts"
        self.repository.checkout_to_branch(branch_to_fix)
        print(instructions.PROMPT_USER_TO_MAKE_FIX)
        self.repository.open_code_in_editor()

        prompt_user.to_press_enter_after_making_changes()
        self.__attempt_to_commit_until_successful(fix_message, challenge_request_issue)
        print("Cherry picking challenge...")
        CherryPick(
            self.repository, is_manual=False, branches=cherry_pick_branches
        ).across_all_branches()

        return FixResult(
            [fix_message],
            True,
            False,
        )

    def __attempt_to_commit_until_successful(
        self, fix_message: str, challenge_request_issue: ChallengeRequestIssue
    ) -> None:
        result_messages = []

        while len(result_messages) == 0:
            try:
                result_messages = self.__commit_changes(
                    fix_message, challenge_request_issue
                )

            except GitCommandError:
                print(instructions.PROMPT_USER_THAT_NO_FIX_WAS_MADE)
                prompt_user.to_press_enter()

    def __commit_changes(
        self, fix_message: str, challenge_request_issue: ChallengeRequestIssue
    ):
        issue_messages = []
        self.repository.add_changes()
        message = self.__add_challenge_request_id_to_message(
            fix_message, challenge_request_issue
        )
        self.repository.commit_changes_with_message(message)
        issue_messages.append(f"{self.repository.get_current_branch()}: {fix_message}")

        return issue_messages

    def __add_challenge_request_id_to_message(
        self, fix_message: str, challenge_request_issue: ChallengeRequestIssue
    ) -> str:
        message = challenge_request_issue.get_issue_id() + ": " + fix_message
        return str(message)
