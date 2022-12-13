import re

from bugfixpy import jira, cms
from bugfixpy.jira import api, Issue


def is_valid_issue(issue: Issue) -> bool:
    issue_id = issue.get_issue_id()
    return is_valid_issue_id(issue_id) and api.issue_exists(issue)


def is_valid_issue_id(issue_id) -> bool:
    return len(issue_id) < 5 and len(issue_id) > 1 and issue_id.isdigit()


def is_valid_challenge_id(cid) -> bool:
    # Checks for 24 character string made up of lower case characters and digits
    return bool(re.fullmatch("^([a-z0-9]{24})", cid))


def is_valid_fix_message(message) -> bool:
    return not is_empty_string(message)


def is_valid_repository_name(repository) -> bool:
    return not is_empty_string(repository)


def is_empty_string(string) -> bool:
    return string == ""


def has_valid_credentials() -> bool:
    if not credentials_are_loaded():
        return False

    response_code = api.get_response_code_from_query_to_verify_credentials()

    if response_code != 200:
        print("Invalid API credentials: Invalid email or permissions on account")
        print("confirm your credentials are correct")
        print("run bug-fix.py --setup to change credentials")
        return False

    return True


def credentials_are_loaded() -> bool:
    return (
        jira.constants.API_EMAIL != ""
        and jira.constants.API_KEY != ""
        and cms.constants.EMAIL != ""
        and cms.constants.PASSWORD != ""
    )
