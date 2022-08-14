import re
from bugfixpy import jira_api
from bugfixpy.constants import cms, jira


def is_valid_ticket_number(ticket):
    """
    Validate ticket number input format
    """
    return len(ticket) < 5 and len(ticket) > 1 and ticket.isdigit()


def is_valid_chlrq(chlrq):
    """
    Validate CHLRQ format and through Jira API
    """
    is_valid = False

    # Confirm chlrq is valid number and is a chlrq in Jira
    if chlrq and is_valid_ticket_number(chlrq) and jira_api.check_chlrq_exists(chlrq):
        is_valid = True

    return is_valid


def is_valid_chlc(chlc):
    """
    Validate CHLC format and through Jira API
    """
    is_valid = False

    # Confirm chlc is valid number and is a chlc in Jira
    if chlc and is_valid_ticket_number(chlc) and jira_api.check_chlc_exists(chlc):
        is_valid = True

    return is_valid


# TODO: finish method
def is_valid_challenge_id(cid) -> bool:
    """
    Check whether the challenge id is valid or not
    """
    # Regex string checks for 24 character string made up of lower case characters and digits
    return bool(re.match("^([a-z0-9]{24})", cid))


def has_credentials():
    """
    Validate that API and CMS credentials exists. Notify user if not
    """
    if not jira.API_EMAIL or not jira.API_KEY or not cms.EMAIL or not cms.PASSWORD:

        return False

    return True


def is_valid_fix_message(message) -> bool:
    """
    Validates fix message. If no message return false, otherwise return true
    """
    return bool(message)


def is_valid_repository_name(repository) -> bool:
    """
    Validates if input is a valid repository
    """
    return bool(repository)
