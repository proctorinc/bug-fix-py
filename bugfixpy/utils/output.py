from typing import List
from bugfixpy.constants import colors

# from src.constants import colors
# from . import Text


def warn_user_of_merge_conflict(branch):
    """Alert user that merge conflict has occurred"""
    print(
        f"{colors.WARNING}[ !!! ]{colors.ENDC} {branch}: {colors.WARNING}MERGE CONFLICT"
    )

def print_fix_messages(fix_messages: List[str]) -> None:
    """
    Print fix message
    """
    for message in fix_messages:
        print(f"{colors.WHITE}\t{message}{colors.ENDC}")


def print_missing_credentials() -> None:
    """Print missing credentials"""
    print("missing credentials")
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
