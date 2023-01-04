from bugfixpy.git import FixResult, FixBranches
from bugfixpy.utils import prompt_user
from bugfixpy.jira import ChallengeRequestIssue, TransitionIssues

from .runnable_mode import RunnableMode
from .scraper_mode import ScraperMode
from .repository_mode import RepositoryMode

from . import utils


class AutomaticMode(RunnableMode, RepositoryMode, ScraperMode):

    __fix_result: FixResult
    __challenge_request_issue: ChallengeRequestIssue

    def __init__(self, test_mode) -> None:
        super().__init__("AUTO", test_mode)

    def run(self) -> None:
        test_mode = self.get_test_mode()
        self.run_scraper()
        self.clone_repository_from_scraper_data()
        self.prompt_user_for_challenge_request_issue()
        self.fix_branches_in_repository()
        self.push_fix_to_github_if_not_in_test_mode(test_mode)
        self.transition_challenge_issues_with_results()

    def clone_repository_from_scraper_data(self) -> None:
        repository_name = self.get_scraper_data().application.repository_name
        self.clone_repository(repository_name)

    def prompt_user_for_challenge_request_issue(self) -> None:
        self.__challenge_request_issue = prompt_user.get_challenge_request_issue()

    def fix_branches_in_repository(self) -> None:
        self.__fix_result = FixBranches(
            self.get_repository(), self.__challenge_request_issue
        ).get_results()

    def transition_challenge_issues_with_results(self) -> None:
        TransitionIssues(
            self.__fix_result,
            self.scraper_data,
            self.__challenge_request_issue,
        ).run()

    def display_results(self) -> None:
        is_chunk_fixing_required = self.__fix_result.is_chunk_fixing_required
        utils.print_end_instructions_based_off_of_results(is_chunk_fixing_required)
