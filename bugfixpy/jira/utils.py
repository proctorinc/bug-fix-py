"""Utility functions for jira class"""

from typing import List
from bugfixpy.constants import jira

INWARD_ISSUE = "outwardIssue"
OUTWARD_ISSUE = "inwardIssue"


def append_project_type_if_not_present(
    valid_issue_number: str, project_type: str
) -> str:

    if project_type not in valid_issue_number:
        return f"{project_type}-{valid_issue_number}"

    return valid_issue_number


def parse_linked_issues(issue_links) -> List[str]:
    """
    Parses json issue links and returns list of all linked CHLC's
    """
    chlcs = []
    issue = ""
    for link in issue_links:
        if OUTWARD_ISSUE in link:
            issue = str(link[OUTWARD_ISSUE][jira.RESPONSE_KEY])
        elif INWARD_ISSUE in link:
            issue = str(link[INWARD_ISSUE][jira.RESPONSE_KEY])

        if issue and "CHLC-" in issue:
            chlcs.append(issue)

    return chlcs
