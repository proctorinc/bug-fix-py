from bugfixpy.git import FixResult
from bugfixpy.jira import TransitionIssues
from bugfixpy.utils import prompt_user
from . import utils


class TransitionIssuesMode:
    @staticmethod
    def run() -> None:
        challenge_data = utils.scrape_challenge_data_from_cms()
        challenge_request_issue = prompt_user.get_challenge_request_issue()

        is_bulk_transition_required = prompt_user.if_bulk_transition_is_required()

        fix_message = prompt_user.for_descripton_of_fix()

        TransitionIssues(
            FixResult([fix_message], is_bulk_transition_required, False),
            challenge_data,
            challenge_request_issue,
        ).run()
