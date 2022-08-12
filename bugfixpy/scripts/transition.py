from typing import List
from bugfixpy.utils import user_input
from bugfixpy import jira_api
from bugfixpy.constants import colors


def transition_jira_issues(
    chlrq: str, fix_messages: List[str], is_cherrypick_required: bool
):
    """
    Use Jira API to transition tickets through Jira workflow
    """
    # API call to get current version name and id
    fixVersionName, fix_version_id = jira_api.get_current_fix_version()

    # Format fix messages
    fix_message = user_input.format_messages(fix_messages)

    # Check that version id was successfully got
    if not fix_version_id:
        # Print error
        print(
            "Unable to determine fix version. Cannot auto-transition tickets. Exiting."
        )
        exit(1)

    # Transitioning CHLRQ
    print(f"\nTransitioning {colors.OKCYAN}CHLRQ-{chlrq}{colors.ENDC}")

    # Transition to in planned, include fix version
    print(f"\tTo Planned [Fix Version: {fixVersionName}]", end="")

    # If api returns 204, transition was successful
    plannedResult = jira_api.transition_issue_to_planned(chlrq, fix_version_id)
    if plannedResult.status_code == 204:
        print(f"\t{colors.OKGREEN}[COMPLETE]{colors.ENDC}")
    else:
        print(
            f"\t{colors.FAIL}[FAILED - {plannedResult.status_code}: {plannedResult.reason}]{colors.ENDC}"
        )

    # Transition to in progress
    print("\tTo In Progress", end="")

    # If api returns 204, transition was successful
    inProgressResult = jira_api.transition_issue_to_in_progress(chlrq)
    if inProgressResult.status_code == 204:
        print(f"\t\t\t\t{colors.OKGREEN}[COMPLETE]{colors.ENDC}")
    else:
        print(
            f"\t\t\t\t{colors.FAIL}[FAILED - {inProgressResult.status_code}: {inProgressResult.reason}]{colors.ENDC}"
        )

    # Transition CHLRQ to closed w/ fix message
    print("\tTo Closed [with description of fix]", end="")

    # If api returns 204, transition was successful
    closedResult = jira_api.transition_issue_to_closed(chlrq, fix_message)
    if closedResult.status_code == 204:
        print(f"\t{colors.OKGREEN}[COMPLETE]{colors.ENDC}")
    else:
        print(
            f"\t{colors.FAIL}[FAILED - {closedResult.status_code}: {closedResult.reason}]{colors.ENDC}"
        )

    # If full app and fix was on the secure branch, transition all CHLC's
    if is_cherrypick_required:
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
        # Get challenge chlc
        print("\n[Enter Challenge CHLC]")
        challenge_chlc = user_input.get_chlc()

        # Set challenges to the initial chlc
        challenges = ["CHLC-" + challenge_chlc[-4:]]

    print(
        f"\nTransitioning [{colors.OKCYAN}{len(challenges)}{colors.ENDC}] {colors.HEADER}CHLC's{colors.ENDC}"
    )

    # Transition all challenges
    for challenge in challenges:

        print(f"Transitioning {colors.HEADER}{challenge}{colors.ENDC}:")

        # Transition challenge to Feedback Open
        print("\tTo Feedback Open", end="")

        # If api returns 204, transition was successful
        feedbackOpenResult = jira_api.transition_issue_to_feedback_open(challenge)
        if feedbackOpenResult.status_code == 204:
            print(f"\t\t{colors.OKGREEN}[COMPLETE]{colors.ENDC}")
        else:
            print(
                f"\t\t{colors.FAIL}[FAILED - {feedbackOpenResult.status_code}: {feedbackOpenResult.reason}]{colors.ENDC}"
            )

        # Transition challenge to Feedback Review w/ fix message and set assignee to Thomas
        print("\tTo Feedback Review", end="")

        # If api returns 204, transition was successful
        feedbackReviewResult = jira_api.transition_issue_to_feedback_review(challenge)
        if feedbackReviewResult.status_code == 204:
            print(f"\t\t{colors.OKGREEN}[COMPLETE]{colors.ENDC}")
        else:
            print(
                f"\t\t{colors.FAIL}[FAILED - {feedbackReviewResult.status_code}: {feedbackReviewResult.reason}]{colors.ENDC}"
            )

        # Sets assignee and adds CHLRQ as comment
        print("\tAdding assignee and comment", end="")

        # If api returns 204, transition was successful
        editResult = jira_api.edit_issue_details(challenge, chlrq)
        if editResult.status_code == 204:
            print(f"\t{colors.OKGREEN}[COMPLETE]{colors.ENDC}")
        else:
            print(f"\t{colors.FAIL}[FAILED - {editResult.status_code}]{colors.ENDC}")
            print(f"{colors.FAIL}{editResult.text}")
