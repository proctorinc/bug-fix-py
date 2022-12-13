import webbrowser

from .issue import Issue

from . import constants


def open_issue_in_browser(issue: Issue) -> None:
    webbrowser.open(constants.BULK_TRANSITION_JQL_URL.format(chlc=issue.get_issue_id()))
