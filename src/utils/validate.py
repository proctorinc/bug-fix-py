from operator import truediv
from src import api, constants


def is_valid_ticket_number(ticket):
    """
    Validate ticket number input format
    """
    return len(ticket) < 5 and len(ticket) > 1 and ticket.isdigit()


def is_valid_chlrq(chlrq):
    """
    Validate CHLRQ format and through Jira API
    """
    isValid = False

    # Confirm chlrq is valid number and is a chlrq in Jira
    if chlrq and is_valid_ticket_number(chlrq) and api.check_chlrq_exists(chlrq):
        isValid = True

    return isValid


def is_valid_chlc(chlc):
    """
    Validate CHLC format and through Jira API
    """
    isValid = False

    # Confirm chlc is valid number and is a chlc in Jira
    if chlc and is_valid_ticket_number(chlc) and api.check_chlc_exists(chlc):
        isValid = True

    return isValid


# TODO: finish method
def is_valid_cid(challenge_id):
    """
    Check whether the challenge id is valid or not
    """
    return True


def has_credentials():
    """
    Validate that API and CMS credentials exists. Notify user if not
    """
    if (
        not constants.JIRA_API_EMAIL
        or not constants.JIRA_API_KEY
        or not constants.CMS_EMAIL
        or not constants.CMS_PASSWORD
    ):

        return False

    return True
