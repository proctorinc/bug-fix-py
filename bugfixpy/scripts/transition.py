from typing import Optional
from requests import Response

from bugfixpy.git.fix_result import FixResult
from bugfixpy.jira.fix_version import FixVersion
from bugfixpy.scraper.scraper_data import ScraperData
from bugfixpy.utils import prompt_user
from bugfixpy.jira import api
from bugfixpy.constants import colors
from bugfixpy.jira.issue import (
    ChallengeCreationIssue,
    ChallengeRequestIssue,
)


def transition_jira_issues(
    fix_result: FixResult,
    challenge_data: ScraperData,
    challenge_request_issue: Optional[ChallengeRequestIssue] = None,
) -> None:
    fix_messages = fix_result.fix_messages
    challenge_creation_issue = challenge_data.challenge.chlc
    application_creation_issue = challenge_data.application.chlc
    repo_was_cherrypicked = fix_result.repo_was_cherrypicked
    fix_version = api.get_current_fix_version()
    fix_message = prompt_user.format_messages(fix_messages)

    if not challenge_request_issue:
        challenge_request_issue = prompt_user.get_challenge_request_issue()

    transition_challenge_request_issue(
        challenge_request_issue, fix_version, fix_message
    )

    if repo_was_cherrypicked:

        linked_issues = api.get_challenge_creation_issues_linked_to_application(
            application_creation_issue
        )

    else:
        linked_issues = [challenge_creation_issue]

    transition_chlcs(linked_issues, challenge_request_issue)


def transition_challenge_request_issue(
    challenge_request_issue: ChallengeRequestIssue, fix_version: FixVersion, fix_message
) -> None:
    try:
        input(
            f"\nPress {colors.OKGREEN}[Enter]{colors.ENDC} to auto transition {colors.OKCYAN}{challenge_request_issue.get_issue_id()}{colors.ENDC}"
        )

        print(
            f"\nTransitioning {colors.OKCYAN}{challenge_request_issue.get_issue_id()}{colors.ENDC}"
        )

        # Transition to in planned, include fix version
        print(f"\tTo Planned [Fix Version: {fix_version.name}]", end="")

        # If api returns 204, transition was successful
        planned_result = api.transition_challenge_request_to_planned(
            challenge_request_issue, fix_version
        )
        check_transition_result(planned_result)

        # Transition to in progress
        print("\tTo In Progress\t\t\t", end="")

        # If api returns 204, transition was successful
        in_progress_result = api.transition_challenge_request_to_in_progress(
            challenge_request_issue
        )
        check_transition_result(in_progress_result)

        # Transition CHLRQ to closed w/ fix message
        print("\tTo Closed [with description of fix]", end="")

        # If api returns 204, transition was successful
        closed_result = api.transition_challenge_request_to_closed_with_comment(
            challenge_request_issue, fix_message
        )
        check_transition_result(closed_result)

    except KeyboardInterrupt:
        print(f"{colors.FAIL}\nSkipped auto transitioning{colors.ENDC}")


def transition_chlcs(
    challenge_creation_issues: list[ChallengeCreationIssue],
    challenge_request_issue: ChallengeRequestIssue,
) -> None:
    try:
        input(
            f"\nPress {colors.OKGREEN}[Enter]{colors.ENDC} to auto transition [{colors.OKBLUE}{len(challenge_creation_issues)}{colors.ENDC}] {colors.HEADER}CHLCs{colors.ENDC}"
        )

        for issue in challenge_creation_issues:

            print(f"Transitioning {colors.HEADER}{issue.get_issue_id()}{colors.ENDC}:")
            print("\tTo Feedback Open\t", end="")
            feedback_open_result = api.transition_challenge_creation_to_feedback_open(
                issue
            )
            check_transition_result(feedback_open_result)

            print("\tTo Feedback Review\t", end="")
            feedback_review_result = (
                api.transition_challenge_creation_to_feedback_review(issue)
            )
            check_transition_result(feedback_review_result)

            print("\tAdding assignee and comment", end="")
            edit_result = (
                api.update_challenge_creation_assignee_and_link_challenge_request(
                    issue, challenge_request_issue
                )
            )
            check_transition_result(edit_result)
    except KeyboardInterrupt:
        print(f"{colors.FAIL}\nSkipped auto transitioning{colors.ENDC}")


def check_transition_result(result: Response) -> None:
    if result.status_code == 204:
        print(f"\t{colors.OKGREEN}[COMPLETE]{colors.ENDC}")
    else:
        print(
            f"\t{colors.FAIL}[FAILED - {result.status_code}: {result.reason}]{colors.ENDC}"
        )
