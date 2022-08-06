from bugfixpy import utils
from bugfixpy.constants import colors


def main():
    # If parameter not entered, prompt user for CHRLQ
    chlrq = utils.get_chlrq()

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
    utils.transition_jira_issues(chlrq, [fix_message], did_cherrypick)
