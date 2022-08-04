from src import constants
# from src.constants import colors
# from . import Text

def print_fix_messages(fix_messages):
    for message in fix_messages:
        print(f'{constants.WHITE}\t{message}{constants.ENDC}')

def print_missing_credentials():
    print('missing credentials')
    # Text('Credentials not setup. Run \'bug-fix.py --setup\' to set up environment variables', colors.FAIL).display()

    # # Notify that no email is present
    # if not constants.JIRA_API_EMAIL:
    #     Text('No API email present', colors.FAIL).display()

    # # Notify that no api key is present
    # if not constants.JIRA_API_KEY:
    #     Text('No API key present', colors.FAIL).display()

    # # Notify that no email is present
    # if not constants.CMS_EMAIL:
    #     Text('No CMS email present', colors.FAIL).display()

    # # Notify that no api key is present
    # if not constants.CMS_PASSWORD:
    #     Text('No CMS password present', colors.FAIL).display()