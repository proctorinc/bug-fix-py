import json
import datetime
from datetime import date
import requests
from bugfixpy.constants import colors, jira


def __get_query(endpoint: str):
    """
    Query Jira API with request headers and Authentication
    """
    response = requests.get(
        url=f"{jira.SCW_API_URL}/{endpoint}",
        headers=jira.REQUEST_HEADERS,
        auth=jira.AUTH,
    )

    return response


def __post_query(endpoint: str, body: dict):
    """
    Query Jira API with request headers and Authentication
    """
    response = requests.post(
        url=f"{jira.SCW_API_URL}/{endpoint}",
        headers=jira.REQUEST_HEADERS,
        auth=jira.AUTH,
        json=body,
    )

    return response


# TODO: Separate API call and functionality (move to validate.py)
def has_valid_credentials():
    """
    GET
    Checks if credentials are able to retrieve data from API
    """
    is_valid = True

    try:
        endpoint = "issue/CHLC-1520/"
        response = __get_query(endpoint)
        json_response = json.loads(response.text)

        if "errorMessages" in json_response:
            print("Invalid API credentials: Invalid email or permissions on account")
            print("confirm your credentials are correct")
            print("run bug-fix.py --setup to change credentials")
            is_valid = False

    except json.decoder.JSONDecodeError:
        print("Invalid API credentials: Invalid API key")
        print("run bug-fix.py --setup to change credentials")
        is_valid = False

    return is_valid


# TODO: Move to utils
def get_linked_issues(issue_links):
    """
    Parses json issue links and returns list of all linked CHLC's
    """
    chlcs = []
    issue = ""
    for link in issue_links:
        if "outwardIssue" in link:
            issue = link["outwardIssue"][jira.RESPONSE_KEY]
        elif "inwardIssue" in link:
            issue = link["inwardIssue"][jira.RESPONSE_KEY]

        if issue and "CHLC-" in issue:
            chlcs.append(issue)

    return chlcs


def get_current_fix_version():
    """
    GET
    Gets current fix version based off of the current date
    """
    today = date.today()
    datetime_object = datetime.datetime.strptime(str(today.month), "%m")
    month = datetime_object.strftime("%b")
    version_name = None
    version_id = None

    endpoint = "project/CHLRQ/versions"
    response = __get_query(endpoint)
    json_response = json.loads(response.text)

    for version in json_response:
        if str(today.year) in version["name"] and month in version["name"]:
            version_name = version["name"]
            version_id = version["id"]

    return version_name, version_id


def transition_issue_to_planned(chlrq, fix_version_id):
    """
    POST
    Transition CHLRQ to Planned w/ fix version
    """
    endpoint = f"issue/CHLRQ-{chlrq}/transitions"
    body = {
        "transition": {"id": jira.TRANSITION_PLANNED},
        "update": {"fixVersions": [{"add": {"id": fix_version_id}}]},
    }
    response = __post_query(endpoint, body)

    return response


def transition_issue_to_in_progress(chlrq):
    """
    POST
    Transition CHLRQ to In Progress
    """
    endpoint = f"issue/CHLRQ-{chlrq}/transitions"
    body = {"transition": {"id": jira.TRANSITION_IN_PROGRESS}}
    response = __post_query(endpoint, body)

    return response


# TODO: THIS DOESN'T WORK FOR ALL CHALLENGES!
def get_creation_chlc(chlc):
    """
    GET
    Get parent CHLC's creation CHLC
    """
    endpoint = f"issue/CHLC-{chlc}/"
    response = __get_query(endpoint)
    json_response = json.loads(response.text)

    if response.text:
        json_response = json.loads(response.text)

        if "errorMessages" in json_response:
            print(f"{colors.FAIL}Error getting creation CHLC{colors.ENDC}")

    return json_response["fields"]["parent"][jira.RESPONSE_KEY]


def get_linked_challenges(chlc):
    """
    GET
    Gets creation CHLC's children CHLCs
    """
    endpoint = f"issue/CHLC-{chlc}"
    response = __get_query(endpoint)
    json_response = json.loads(response.text)

    return get_linked_issues(json_response["fields"]["issue_links"])


def link_creation_chlc(chlrq, chlc):
    """
    POST
    Links creation CHLC to CHLRQ
    """
    endpoint = "issueLink"
    body = {
        "type": {"name": "Relates"},
        "outwardIssue": {jira.RESPONSE_KEY: f"CHLRQ-{chlrq}"},
        "inwardIssue": {jira.RESPONSE_KEY: f"CHLC-{chlc}"},
    }

    return __post_query(endpoint, body)


def transition_issue_to_closed(chlrq, comment):
    """
    POST
    Links transitions CHLRQ to closed
    """
    endpoint = f"issue/CHLRQ-{chlrq}/transitions"
    body = {
        "transition": {"id": "191"},
        "update": {"comment": [{"add": {"body": comment}}]},
    }
    return __post_query(endpoint, body)


def transition_issue_to_feedback_open(chlc):
    """
    POST
    Transition CHLC to feedback open
    """
    endpoint = f"issue/{chlc}/transitions"
    body = {"transition": {"id": jira.TRANSITION_FEEDBACK_OPEN}}
    return __post_query(endpoint, body)


def transition_issue_to_feedback_review(chlc):
    """
    POST
    Transition CHLC to feedback review and add comment and change assignee to Thomas
    """
    endpoint = f"issue/{chlc}/transitions"
    body = {"transition": {"id": jira.TRANSITION_FEEDBACK_REVIEW}}
    return __post_query(endpoint, body)


def edit_issue_details(chlc, chlrq):
    """
    PUT
    Jira edit query. Changes CHLC's assignee to Thomas and adds comment
    """
    endpoint = f"issue/{chlc}"
    body = {
        "fields": {"assignee": {"accountId": jira.THOMAS_ACCT_ID}},
        "update": {"comment": [{"add": {"body": f"CHLRQ-{chlrq}"}}]},
    }
    return __post_query(endpoint, body)


def check_chlc_exists(chlc):
    """
    GET
    Confirm that chlc number is valid
    """
    endpoint = f"issue/CHLC-{chlc}/"
    response = __get_query(endpoint)
    json_response = json.loads(response.text)

    return (
        jira.RESPONSE_KEY in json_response
        and jira.CHLC in json_response[jira.RESPONSE_KEY]
    )


def check_chlrq_exists(chlrq):
    """
    GET
    Confirm that chlrq number is valid
    """
    endpoint = f"/issue/CHLRQ-{chlrq}/"
    response = __get_query(endpoint)
    json_response = json.loads(response.text)

    return (
        jira.RESPONSE_KEY in json_response
        and jira.CHRLQ in json_response[jira.RESPONSE_KEY]
    )
