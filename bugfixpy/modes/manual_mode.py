from bugfixpy.git import Repository, FixBranches
from bugfixpy.jira import ChallengeRequestIssue
from bugfixpy.utils import browser, prompt_user, Text
from bugfixpy.utils.text import colors, instructions

from .runnable_mode import RunnableMode


class ManualMode(RunnableMode):

    __repository: Repository
    __challenge_request_issue: ChallengeRequestIssue

    def __init__(self, test_mode: bool) -> None:
        super().__init__("MANUAL", test_mode)

    def run(self) -> None:
        self.initialize_repository_from_user()
        self.get_challenge_request_from_user()
        self.run_fix_on_branches()
        self.push_if_test_mode_disabled()

    def initialize_repository_from_user(self) -> None:
        print(instructions.PROMPT_FOR_REPOSITORY_NAME)
        repository_name = prompt_user.for_repository_name()
        self.__repository = Repository(repository_name)
        self.display_repository_stats()

    def get_challenge_request_from_user(self) -> None:
        print(instructions.PROMPT_FOR_CHALLENGE_REQUEST)
        self.__challenge_request_issue = prompt_user.get_challenge_request_issue()

    def run_fix_on_branches(self) -> None:
        print(instructions.TRANSITION_AND_CHECKOUT_STEPS)
        FixBranches(
            self.__repository, self.__challenge_request_issue, is_manual=True
        ).run_fix()

    def display_repository_stats(self) -> None:
        Text("Repo:", self.__repository, colors.OKCYAN).display()
        Text("Branches:", self.__repository.get_num_branches(), colors.OKCYAN).display()

        if self.__repository.is_full_app():
            Text("Type:", "Full App", colors.OKCYAN).display()
        else:
            Text("Type:", "Minified App", colors.OKCYAN).display()

    def push_if_test_mode_disabled(self) -> None:
        if self.test_mode:
            input(instructions.PROMPT_FOR_ENTER_PUSH_DISABLED)
        else:
            print(instructions.PROMPT_FOR_ENTER_PUSH_ENABLED)
            self.__repository.push_all_branches()

    def display_results(self) -> None:
        print(instructions.CLOSE_CHALLENGE_REQUEST_STEPS)
        self.display_transition_instructions()
        self.display_chunk_fix_instructions()
        print(instructions.BUG_FIX_COMPLETE)

    def display_transition_instructions(self) -> None:
        if self.__repository.was_cherry_picked():
            self.display_cherry_pick_transition_instructions()
        else:
            print(instructions.NO_CHERRY_PICKING_MANUAL_STEPS)

    def display_cherry_pick_transition_instructions(self) -> None:
        application_creation_issue = prompt_user.get_application_creation_issue()
        browser.open_issue_in_browser(application_creation_issue)
        print(instructions.CHERRY_PICKING_MANUAL_STEPS)

    def display_chunk_fix_instructions(self) -> None:
        if self.__repository.did_number_of_lines_change():
            print(instructions.UPDATE_CMS_AND_FIX_CHUNKS_REMINDER)
        else:
            print(instructions.UPDATE_CMS_REMINDER)
