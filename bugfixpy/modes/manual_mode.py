from bugfixpy.git import Repository, FixBranches
from bugfixpy.utils import browser
from bugfixpy.utils import prompt_user, Text, formatter
from bugfixpy.utils.text import colors, instructions
from .runnable_mode import RunnableMode


class ManualMode(RunnableMode):

    __repository: Repository

    def __init__(self, test_mode) -> None:
        super().__init__(test_mode)

    def run(self) -> None:
        repository_name = prompt_user.for_repository_name()
        self.__repository = Repository(repository_name)
        self.display_repository_stats()
        challenge_request_issue = prompt_user.get_challenge_request_issue()
        FixBranches(self.__repository, challenge_request_issue).run_fix()
        self.push_if_test_mode_disabled()

    def display_repository_stats(self) -> None:
        Text("Repo:", self.__repository, colors.OKCYAN).display()
        Text("Branches:", self.__repository.get_num_branches(), colors.OKCYAN).display()

        if self.__repository.is_full_app():
            Text("Type:", "Full App", colors.OKCYAN).display()
        else:
            Text("Type:", "Minified App", colors.OKCYAN).display()

    def push_if_test_mode_disabled(self) -> None:
        if self.test_mode:
            print(instructions.PROMPT_FOR_ENTER_PUSH_DISABLED)
        else:
            print(instructions.PROMPT_FOR_ENTER_PUSH_ENABLED)
            self.__repository.push_all_branches()

    def display_results(self) -> None:
        print(instructions.STEP_ONE_CLOSE_CHLRQ)
        print(formatter.format_fix_messages(self.__repository.get_fix_messages()))
        print(instructions.STEP_TWO_LINK_CHLRQ)

        if self.__repository.was_cherry_picked():

            application_creation_issue = prompt_user.get_application_creation_issue()

            browser.open_issue_in_browser(application_creation_issue)

            print(instructions.CHERRY_PICKING_MANUAL_STEPS)
        else:
            print(instructions.NO_CHERRY_PICKING_MANUAL_STEPS)

        if self.__repository.did_number_of_lines_change():
            print(instructions.UPDATE_CMS_AND_FIX_CHUNKS_REMINDER)
        else:
            print(instructions.UPDATE_CMS_REMINDER)

        print(instructions.BUG_FIX_COMPLETE)
