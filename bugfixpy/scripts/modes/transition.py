from bugfixpy.utils import user_input
from bugfixpy.constants import colors
from bugfixpy.scripts import transition


def run():
    """
    Run method for transition mode
    """
    # If parameter not entered, prompt user for CHRLQ
    challenge_request_issue = user_input.get_challenge_request_issue()

    did_cherrypick = False

    # Ask user if bulk transition is required
    if (
        input(
            f"Is bulk transition required? ({colors.BOLD}{colors.WHITE}Y{colors.ENDC}/n): {colors.WHITE}"
        )
        != "n"
    ):
        did_cherrypick = True

    fix_message = input(f"{colors.ENDC}Enter fix message: {colors.WHITE}")

    print(colors.ENDC)

    # Automatically transition jira tickets
    transition.transition_jira_issues(
        [fix_message], did_cherrypick, challenge_request_issue
    )
