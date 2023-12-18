from bugfixpy.cms import ScraperData
from bugfixpy.git import FixResult, FixBranches
from bugfixpy.utils import prompt_user
from bugfixpy.jira import ChallengeRequestIssue, TransitionIssues

from .types import RunnableMode, ScraperMode, RepositoryMode

from . import utils


class AutomaticMode(RunnableMode, RepositoryMode, ScraperMode):
    MODE = "AUTO"

    __fix_result: FixResult
    __challenge_request_issue: ChallengeRequestIssue

    def __init__(self, test_mode) -> None:
        super().__init__(self.MODE, test_mode)

    def run(self) -> None:
        test_mode = self.get_test_mode()
        challenge_data = self.scrape_challenge_data()
        self.clone_repository_from_scraper_data(challenge_data)
        self.prompt_user_for_challenge_request_issue()
        self.fix_branches_in_repository(challenge_data)
        self.push_fix_to_github_if_not_in_test_mode(test_mode)
        self.transition_challenge_issues_with_results(challenge_data)

    def clone_repository_from_scraper_data(self, challenge_data: ScraperData) -> None:
        repository_name = challenge_data.application.repository_name
        self.clone_repository(repository_name)

    def prompt_user_for_challenge_request_issue(self) -> None:
        self.__challenge_request_issue = prompt_user.get_challenge_request_issue()

    def fix_branches_in_repository(self, challenge_data: ScraperData) -> None:
        branches: list[str] = []
        for challenge in challenge_data.application.challenges:
            branches.append(challenge.secure_branch)
            branches.extend(challenge.vulnerable_branches)

        self.__fix_result = FixBranches(
            self.get_repository(),
            self.__challenge_request_issue,
            branches=branches,
        ).get_results()

    def transition_challenge_issues_with_results(
        self, challenge_data: ScraperData
    ) -> None:
        TransitionIssues(
            self.__fix_result,
            challenge_data,
            self.__challenge_request_issue,
        ).run()

    def display_results(self) -> None:
        is_chunk_fixing_required = self.__fix_result.is_chunk_fixing_required
        utils.print_end_instructions_based_off_of_results(is_chunk_fixing_required)
