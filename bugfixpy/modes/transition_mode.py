from bugfixpy.git import FixResult
from bugfixpy.jira import TransitionIssues
from bugfixpy.utils import prompt_user

from .types import RunnableMode, ScraperMode


class TransitionMode(RunnableMode, ScraperMode):

    MODE = "TRANSITION"

    def __init__(self) -> None:
        super().__init__(self.MODE, test_mode=False)

    def run(self) -> None:
        self.scrape_challenge_data()
        challenge_request_issue = prompt_user.get_challenge_request_issue()

        is_bulk_transition_required = prompt_user.if_bulk_transition_is_required()

        fix_message = prompt_user.for_descripton_of_fix()

        TransitionIssues(
            FixResult([fix_message], is_bulk_transition_required, False),
            self.scrape_challenge_data(),
            challenge_request_issue,
        ).run()

    def display_results(self) -> None:
        print("Transitioning complete.")
