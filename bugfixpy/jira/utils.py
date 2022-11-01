import json
from datetime import datetime, date
from typing import List

from bugfixpy.constants import jira
from .fix_version import FixVersion

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


def project_type_exists_in_response(project_type, response) -> bool:
    json_response = json.loads(response.text)
    return (
        jira.RESPONSE_KEY in json_response
        and project_type in json_response[jira.RESPONSE_KEY]
    )


def parse_application_creation_from_response(response) -> str:
    json_response = json.loads(response.text)

    return str(json_response["fields"]["parent"][jira.RESPONSE_KEY])


def parse_linked_challenges_from_response(response) -> List[str]:
    json_response = json.loads(response.text)
    return parse_linked_issues(json_response["fields"]["issuelinks"])


def parse_fix_version_from_response(response) -> FixVersion:
    json_response = json.loads(response.text)
    version_id = ""
    version_name = ""
    today = date.today()
    datetime_object = datetime.strptime(str(today.month), "%m")
    month = datetime_object.strftime("%b")

    for version in json_response:
        if str(today.year) in version["name"] and month in version["name"]:
            version_name = version["name"]
            version_id = version["id"]

    return FixVersion(version_id=version_id, version_name=version_name)
