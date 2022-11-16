from bugfixpy.git.fix_result import FixResult
from bugfixpy.utils import prompt_user
from bugfixpy.scripts import transition
from bugfixpy.scripts.modes.utils import scrape_challenge_data_from_cms


def run() -> None:
    challenge_data = scrape_challenge_data_from_cms()
    challenge_request_issue = prompt_user.get_challenge_request_issue()

    is_bulk_transition_required = prompt_user.if_bulk_transition_is_required()

    fix_message = prompt_user.for_descripton_of_fix()

    transition.transition_jira_issues(
        FixResult([fix_message], is_bulk_transition_required, False),
        challenge_data,
        challenge_request_issue,
    )
