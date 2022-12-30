from bugfixpy.git import FixResult, Repository, FixBranches
from bugfixpy.utils.text import colors, instructions
from bugfixpy.cms import ScraperData
from bugfixpy.utils import prompt_user
from bugfixpy.jira import ChallengeRequestIssue, TransitionIssues

from .runnable_mode import RunnableMode
from .use_scraper import UseScraper

from . import utils


class AutomaticMode(RunnableMode, UseScraper):

    test_mode: bool
    challenge_data: ScraperData
    fix_result: FixResult
    challenge_request_issue: ChallengeRequestIssue
    repository: Repository

    def __init__(self, test_mode) -> None:
        super().__init__("AUTO", test_mode)
        self.test_mode = test_mode

    def run(self) -> None:
        # self.challenge_data = utils.scrape_challenge_data_from_cms(self.challenge_id)
        self.run_scraper()
        repository = utils.clone_the_challenge_repository(
            self.get_scraper_data().application.repository_name
        )
        self.set_repository(repository)
        challenge_request_issue = prompt_user.get_challenge_request_issue()
        self.set_challenge_request_issue(challenge_request_issue)
        self.fix_result = FixBranches(repository, challenge_request_issue).get_results()
        self.push_fix_to_github_if_not_in_test_mode()
        self.transition_challenge_issues_with_results()

    def display_results(self) -> None:
        utils.print_end_instructions_based_off_of_results(self.fix_result)

    def set_repository(self, repository: Repository) -> None:
        self.repository = repository

    def set_challenge_data(self, challenge_data: ScraperData) -> None:
        self.challenge_data = challenge_data

    def set_challenge_request_issue(
        self, challenge_request_issue: ChallengeRequestIssue
    ) -> None:
        self.challenge_request_issue = challenge_request_issue

    def push_fix_to_github_if_not_in_test_mode(self) -> None:
        try:
            if self.test_mode:
                print(f"{colors.HEADER}Test mode enabled. Push skipped{colors.ENDC}")
            else:
                input(instructions.PROMPT_FOR_ENTER_PUSH_ENABLED)
                self.repository.push_all_branches()
        except KeyboardInterrupt:
            print(f"\n{colors.FAIL}Skipped push to repository{colors.ENDC}")

    def transition_challenge_issues_with_results(
        self,
    ) -> None:
        TransitionIssues(
            self.fix_result,
            self.scraper_data,
            self.challenge_request_issue,
        ).run()
