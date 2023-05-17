from typing import List
import requests
from requests import Response

from bugfixpy.jira import (
    Issue,
    ChallengeRequestIssue,
    ChallengeCreationIssue,
    ApplicationCreationIssue,
)

from .fix_version import FixVersion
from . import utils
from . import constants


def __execute_get_query(endpoint: str) -> Response:
    response = requests.get(
        url=f"{constants.SCW_API_URL}/{endpoint}",
        headers=constants.REQUEST_HEADERS,
        auth=constants.AUTH,
    )
    return response


def __execute_post_query(endpoint: str, body: dict) -> Response:
    response = requests.post(
        url=f"{constants.SCW_API_URL}/{endpoint}",
        headers=constants.REQUEST_HEADERS,
        auth=constants.AUTH,
        json=body,
    )
    return response


def __execute_put_query(endpoint: str, body: dict) -> Response:
    response = requests.put(
        url=f"{constants.SCW_API_URL}/{endpoint}",
        headers=constants.REQUEST_HEADERS,
        auth=constants.AUTH,
        json=body,
    )
    return response


def get_response_code_from_query_to_verify_credentials() -> int:
    challenge_creation: ChallengeCreationIssue = ChallengeCreationIssue("CHLC-1520")
    endpoint = challenge_creation.get_issue_endpoint()
    response = __execute_get_query(endpoint)

    return response.status_code


def get_current_fix_version() -> FixVersion:
    endpoint = constants.LINKED_ISSUES_ENDPOINT
    response = __execute_get_query(endpoint)

    return utils.parse_fix_version_from_response(response)


def issue_exists(issue: Issue) -> bool:
    endpoint = issue.get_issue_endpoint()
    response = __execute_get_query(endpoint)

    return utils.project_type_exists_in_response(issue.get_project_type(), response)


def transition_challenge_request_to_planned(
    challenge_request_issue: ChallengeRequestIssue, fix_version: FixVersion
) -> Response:
    endpoint = challenge_request_issue.get_transition_endpoint()
    body = get_transition_to_planned_body(fix_version.id_)
    response = __execute_post_query(endpoint, body)

    return response


def get_transition_to_planned_body(fix_version_id) -> dict:
    return {
        "transition": {"id": constants.TRANSITION_PLANNED},
        "update": {"fixVersions": [{"add": {"id": fix_version_id}}]},
    }


def transition_challenge_request_to_in_progress(
    challenge_request_issue: ChallengeRequestIssue,
) -> Response:
    endpoint = challenge_request_issue.get_transition_endpoint()
    body = get_transition_to_in_progress_body()
    response = __execute_post_query(endpoint, body)

    return response


def get_transition_to_in_progress_body() -> dict:
    return {"transition": {"id": constants.TRANSITION_IN_PROGRESS}}


def get_application_creation_related_to_challenge(
    challenge_creation_issue: ChallengeCreationIssue,
) -> ApplicationCreationIssue:
    endpoint = challenge_creation_issue.get_issue_endpoint()
    response = __execute_get_query(endpoint)
    application_creation_id = utils.parse_application_creation_from_response(response)

    return ApplicationCreationIssue(application_creation_id)


def get_challenge_creation_issues_linked_to_application(
    application_creation_issue: ApplicationCreationIssue,
) -> List[ChallengeCreationIssue]:
    endpoint = application_creation_issue.get_issue_endpoint()
    response = __execute_get_query(endpoint)
    challenge_creation_ids = utils.parse_linked_challenges_from_response(response)

    return [ChallengeCreationIssue(id) for id in challenge_creation_ids]


def link_challenge_request_to_challenge_creation_(
    challenge_request_issue: ChallengeRequestIssue,
    challenge_creation_issue: ChallengeCreationIssue,
) -> Response:
    endpoint = constants.LINKED_ISSUES_ENDPOINT
    body = get_issue_link_body(challenge_request_issue, challenge_creation_issue)

    return __execute_post_query(endpoint, body)


def get_issue_link_body(
    challenge_request_issue: ChallengeRequestIssue,
    challenge_creation_issue: ChallengeCreationIssue,
) -> dict:
    return {
        "type": {"name": "Relates"},
        "outwardIssue": {
            constants.RESPONSE_KEY: challenge_request_issue.get_issue_id()
        },
        "inwardIssue": {
            constants.RESPONSE_KEY: challenge_creation_issue.get_issue_id()
        },
    }


def transition_challenge_request_to_closed_with_comment(
    challenge_request_issue: ChallengeRequestIssue, comment
) -> Response:
    endpoint = challenge_request_issue.get_transition_endpoint()
    body = get_transition_closed_with_comment_body(comment)

    return __execute_post_query(endpoint, body)


def get_transition_closed_with_comment_body(comment: str) -> dict:
    return {
        "transition": {"id": constants.TRANSITION_TO_CLOSED_ID},
        "update": {"comment": [{"add": {"body": comment}}]},
    }


def transition_challenge_creation_to_feedback_open(
    challenge_creation_issue: ChallengeCreationIssue,
) -> Response:
    endpoint = challenge_creation_issue.get_transition_endpoint()
    body = get_feedback_open_body()

    return __execute_post_query(endpoint, body)


def get_feedback_open_body() -> dict:
    return {"transition": {"id": constants.TRANSITION_FEEDBACK_OPEN}}


def transition_challenge_creation_to_feedback_review(
    challenge_creation_issue: ChallengeCreationIssue,
) -> Response:
    endpoint = challenge_creation_issue.get_transition_endpoint()
    body = get_feedback_review_body()

    return __execute_post_query(endpoint, body)


def get_feedback_review_body() -> dict:
    return {"transition": {"id": constants.TRANSITION_FEEDBACK_REVIEW}}


def update_challenge_creation_assignee_and_link_challenge_request(
    challenge_creation_issue: ChallengeCreationIssue,
    challenge_request_issue: ChallengeRequestIssue,
    content_verifier_id: str,
) -> Response:
    endpoint = challenge_creation_issue.get_issue_endpoint()
    body = get_update_challenge_request_body(
        challenge_request_issue, content_verifier_id
    )

    return __execute_put_query(endpoint, body)


def get_update_challenge_request_body(
    challenge_request: ChallengeRequestIssue,
    content_verifier_id: str,
) -> dict:
    challenge_request_id = challenge_request.get_issue_id()
    return {
        "fields": {"assignee": {"accountId": content_verifier_id}},
        "update": {"comment": [{"add": {"body": challenge_request_id}}]},
    }
