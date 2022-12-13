import sys

from bugfixpy.classes import UseScraper
from bugfixpy.git import FixResult, Repository, FixBranches
from bugfixpy.utils.text import colors, instructions
from bugfixpy.cms import ScraperData
from bugfixpy.scripts import transition
from bugfixpy.utils import prompt_user
from bugfixpy.jira import (
    ChallengeRequestIssue,
)
from . import utils


class AutomaticFix(UseScraper):

    test_mode: bool
    challenge_data: ScraperData
    fix_result: FixResult
    challenge_request_issue: ChallengeRequestIssue
    repository: Repository

    def __init__(self, test_mode) -> None:
        super().__init__()
        self.test_mode = test_mode
        self.challenge_data = None

    @classmethod
    def run(cls, test_mode: bool) -> None:
        auto_fix = cls(test_mode)
        utils.print_mode_headers(test_mode)

        # challenge_data = utils.scrape_challenge_data_from_cms()
        # auto_fix.set_challenge_data(challenge_data)
        auto_fix.run_scraper()
        repository = utils.clone_the_challenge_repository(
            # challenge_data.application.repository_name
            auto_fix.get_scraper_data().application.repository_name
        )
        auto_fix.set_repository(repository)
        challenge_request_issue = prompt_user.get_challenge_request_issue()
        auto_fix.set_challenge_request_issue(challenge_request_issue)
        fix_result = FixBranches(repository, challenge_request_issue).get_results()
        auto_fix.set_fix_result(fix_result)
        auto_fix.push_fix_to_github_if_not_in_test_mode()
        auto_fix.transition_challenge_issues_with_results()

        utils.print_end_instructions_based_off_of_results(fix_result)

    def set_repository(self, repository: Repository) -> None:
        self.repository = repository

    def set_fix_result(self, fix_result: FixResult) -> None:
        self.fix_result = fix_result

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
        try:
            transition.transition_jira_issues(
                self.fix_result,
                self.challenge_data,
                self.challenge_request_issue,
            )

        except Exception as err:
            print(err)
            sys.exit(1)
