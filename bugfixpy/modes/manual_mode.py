from bugfixpy.git import FixBranches
from bugfixpy.jira import ChallengeRequestIssue
from bugfixpy.utils import browser, prompt_user
from bugfixpy.utils.text import instructions

from .runnable_mode import RunnableMode
from .repository_mode import RepositoryMode


class ManualMode(RunnableMode, RepositoryMode):

    __challenge_request_issue: ChallengeRequestIssue

    def __init__(self, test_mode: bool) -> None:
        super().__init__("MANUAL", test_mode)

    def run(self) -> None:
        test_mode = self.get_test_mode()
        self.instruct_user_to_clone_repository()
        self.get_challenge_request_from_user()
        self.run_fix_on_branches()
        self.push_fix_to_github_if_not_in_test_mode(test_mode)

    def instruct_user_to_clone_repository(self) -> None:
        print(instructions.PROMPT_FOR_REPOSITORY_NAME)
        self.clone_repository_from_user_input()
        self.print_repository_details()

    def get_challenge_request_from_user(self) -> None:
        print(instructions.PROMPT_FOR_CHALLENGE_REQUEST)
        self.__challenge_request_issue = prompt_user.get_challenge_request_issue()

    def run_fix_on_branches(self) -> None:
        print(instructions.TRANSITION_AND_CHECKOUT_STEPS)
        FixBranches(
            self.get_repository(), self.__challenge_request_issue, is_manual=True
        ).run_fix()

    def display_results(self) -> None:
        print(instructions.CLOSE_CHALLENGE_REQUEST_STEPS)
        self.display_transition_instructions()
        self.display_chunk_fix_instructions()
        print(instructions.BUG_FIX_COMPLETE)

    def display_transition_instructions(self) -> None:
        repository = self.get_repository()
        if repository.was_cherry_picked():
            self.display_cherry_pick_transition_instructions()
        else:
            print(instructions.NO_CHERRY_PICKING_MANUAL_STEPS)

    def display_cherry_pick_transition_instructions(self) -> None:
        application_creation_issue = prompt_user.get_application_creation_issue()
        browser.open_issue_in_browser(application_creation_issue)
        print(instructions.CHERRY_PICKING_MANUAL_STEPS)

    def display_chunk_fix_instructions(self) -> None:
        repository = self.get_repository()
        if repository.did_number_of_lines_change():
            print(instructions.UPDATE_CMS_AND_FIX_CHUNKS_REMINDER)
        else:
            print(instructions.UPDATE_CMS_REMINDER)
