from src import utils, constants

def main():
    # If parameter not entered, prompt user for CHRLQ
    chlrq = utils.get_chlrq()

    # Ask user if bulk transition is required
    if input(f'Is bulk transition required? ({constants.BOLD}{constants.WHITE}Y{constants.ENDC}/n): {constants.WHITE}') != 'n':
        did_cherrypick = True

    fix_messages = input(f'{constants.ENDC}Enter fix message: {constants.WHITE}')

    print(constants.ENDC)

    # Automatically transition jira tickets
    utils.transition_jira_issues(chlrq, fix_messages, did_cherrypick)
