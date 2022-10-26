from typing import List

from requests import Response
from bugfixpy.utils import user_input
from bugfixpy import jira_api
from bugfixpy.constants import colors


def transition_jira_issues(
    fix_messages: List[str],
    is_cherrypick_required: bool,
    chlrq=None,
    challenge_chlc=None,
    application_chlc=None,
) -> None:
    """
    Use Jira API to transition tickets through Jira workflow
    """
    # API call to get current version name and id
    fix_version_name, fix_version_id = jira_api.get_current_fix_version()

    # Format fix messages
    fix_message = user_input.format_messages(fix_messages)

    # Check that version id was successfully got
    if not fix_version_id:
        raise Exception(
            "Unable to determine fix version. Cannot auto-transition tickets. Exiting."
        )

    # If parameter not entered, prompt user for CHRLQ
    if not chlrq:
        chlrq = user_input.get_chlrq()

    transition_chlrq(chlrq, fix_version_name, fix_version_id, fix_message)

    # If full app and fix was on the secure branch, transition all CHLC's
    if is_cherrypick_required:

        if not application_chlc:
            # Get application CHLC
            print("\n[Enter Application CHLC]")
            application_chlc = user_input.get_chlc()

        # Notify user of parent CHLC number
        print(f"Application CHLC: {colors.WARNING}{application_chlc}{colors.ENDC}")

        # Get all CHLC's linked to the creation ticket
        challenges = jira_api.get_linked_challenges(application_chlc)

        # Print number of challenges to bulk transition
        print(f"Challenges to bulk transition: {len(challenges)}")

    else:
        if not challenge_chlc:
            # Get challenge chlc
            print("\n[Enter Challenge CHLC]")
            challenge_chlc = user_input.get_chlc()

        # Set challenges to the initial chlc
        challenges = ["CHLC-" + challenge_chlc[-4:]]

    transition_chlcs(challenges, chlrq)


def transition_chlrq(chlrq: str, fix_version_name, fix_version_id, fix_message) -> None:
    """
    Transition CHLRQ issue through Jira API and print results
    """
    # Transitioning CHLRQ
    print(f"\nTransitioning {colors.OKCYAN}CHLRQ-{chlrq}{colors.ENDC}")

    # Transition to in planned, include fix version
    print(f"\tTo Planned [Fix Version: {fix_version_name}]", end="")

    # If api returns 204, transition was successful
    planned_result = jira_api.transition_issue_to_planned(chlrq, fix_version_id)
    check_transition_result(planned_result)

    # Transition to in progress
    print("\tTo In Progress\t\t\t", end="")

    # If api returns 204, transition was successful
    in_progress_result = jira_api.transition_issue_to_in_progress(chlrq)
    check_transition_result(in_progress_result)

    # Transition CHLRQ to closed w/ fix message
    print("\tTo Closed [with description of fix]", end="")

    # If api returns 204, transition was successful
    closed_result = jira_api.transition_issue_to_closed(chlrq, fix_message)
    check_transition_result(closed_result)


def transition_chlcs(challenges, chlrq) -> None:
    """
    Transition all chlc's related to the given challenge using the Jira API
    """

    print(
        f"\nTransitioning [{colors.OKCYAN}{len(challenges)}{colors.ENDC}] {colors.HEADER}CHLC's{colors.ENDC}"
    )

    # Transition all challenges
    for challenge in challenges:

        print(f"Transitioning {colors.HEADER}{challenge}{colors.ENDC}:")

        # Transition challenge to Feedback Open
        print("\tTo Feedback Open", end="")

        # If api returns 204, transition was successful
        feedback_open_result = jira_api.transition_issue_to_feedback_open(challenge)
        check_transition_result(feedback_open_result)

        # Transition challenge to Feedback Review w/ fix message and set assignee to Thomas
        print("\tTo Feedback Review", end="")

        # If api returns 204, transition was successful
        feedback_review_result = jira_api.transition_issue_to_feedback_review(challenge)
        check_transition_result(feedback_review_result)

        # Sets assignee and adds CHLRQ as comment
        print("\tAdding assignee and comment", end="")

        # If api returns 204, transition was successful
        edit_result = jira_api.edit_issue_details(challenge, chlrq)
        check_transition_result(edit_result)


def check_transition_result(result: Response) -> None:
    """
    Prints whether transitioning the issue was successful or not
    """
    if result.status_code == 204:
        print(f"\t\t{colors.OKGREEN}[COMPLETE]{colors.ENDC}")
    else:
        print(
            f"\t\t{colors.FAIL}[FAILED - {result.status_code}: {result.reason}]{colors.ENDC}"
        )
