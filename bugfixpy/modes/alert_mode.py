from bugfixpy.cms import (
    ApplicationScreenDataWithChallengeBranches,
)
from bugfixpy.git import FixResult, RepoFixer
from bugfixpy.jira import (
    TransitionIssueService,
)
from bugfixpy.utils import prompt_user
from bugfixpy.jira import ChallengeRequestIssue
from bugfixpy.utils.text import colors

from .types import RunnableMode, ScraperMode, RepositoryMode

from . import utils


class AlertMode(RunnableMode, RepositoryMode, ScraperMode):
    MODE = "ALERT"

    __fix_result: FixResult

    def __init__(self, test_mode) -> None:
        super().__init__(self.MODE, test_mode)

    def run(self) -> None:
        test_mode = self.get_test_mode()
        application_data = self.scrape_application_data()
        self.clone_repository_from_scraper_data(application_data)
        challenge_request_issue = prompt_user.get_challenge_request_issue()
        self.fix_branches_in_repository(application_data, challenge_request_issue)
        self.push_fix_to_github_if_not_in_test_mode(test_mode)
        self.transition_challenge_issues_with_results(
            challenge_request_issue, application_data
        )

    def clone_repository_from_scraper_data(
        self, application_data: ApplicationScreenDataWithChallengeBranches
    ) -> None:
        repository_name = application_data.repository_name
        self.clone_repository(repository_name)

    def fix_branches_in_repository(
        self,
        application_data: ApplicationScreenDataWithChallengeBranches,
        challenge_request_issue: ChallengeRequestIssue,
    ) -> None:
        repo_fixer = RepoFixer(
            self.get_repository(),
        )

        if self.is_repo_full_app():
            print(f"{colors.HEADER}Running Full App Fix{colors.ENDC}")
            all_branches = []

            for challenge_key in application_data.challenge_map.keys():
                all_branches.extend(
                    application_data.challenge_map[challenge_key].vulnerable_branches
                )

            self.__fix_result = repo_fixer.fix_branch_and_cherry_pick(
                "secure",
                all_branches,
                challenge_request_issue,
            )

        else:
            print(f"{colors.HEADER}Running Minified Fix{colors.ENDC}")
            for challenge_key in application_data.challenge_map.keys():
                secure_branch = application_data.challenge_map[
                    challenge_key
                ].secure_branch
                print(
                    f"\n\n{colors.OKCYAN}Fixing secure branch: {colors.WHITE}{colors.BOLD}{secure_branch}{colors.ENDC}"
                )
                self.__fix_result = repo_fixer.fix_branch_and_cherry_pick(
                    secure_branch,
                    application_data.challenge_map[challenge_key].vulnerable_branches,
                    challenge_request_issue,
                )

    def transition_challenge_issues_with_results(
        self,
        challenge_request_issue: ChallengeRequestIssue,
        application_data: ApplicationScreenDataWithChallengeBranches,
    ) -> None:
        transition_service = TransitionIssueService()

        transition_service.transition_chrlq(
            challenge_request_issue, "Fixed vulnerable packages per dependabot alerts"
        )

        transition_service.transition_all_chlcs(
            application_data.chlc, challenge_request_issue
        )

    def display_results(self) -> None:
        is_chunk_fixing_required = self.__fix_result.is_chunk_fixing_required
        utils.print_end_instructions_based_off_of_results(is_chunk_fixing_required)
