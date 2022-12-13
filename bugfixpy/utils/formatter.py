from typing import List
from .text import colors


def combine_messages_into_string(messages: List[str]) -> str:
    formatted_message = ""
    for i, message in enumerate(messages):
        if message != "-":
            if i < len(messages) - 1:
                formatted_message += message + "\n"
            else:
                formatted_message += message

    return formatted_message


def format_fix_messages(fix_messages: List[str]) -> str:
    """
    Print fix message
    """
    formatted_message = ""
    for message in fix_messages:
        formatted_message += f"{colors.WHITE}\t{message}{colors.ENDC}"

    return formatted_message


def format_missing_credentials() -> str:
    """Print missing credentials"""
    return "missing credentials"
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
