from bugfixpy.jiraapi import JiraApi
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
    if chlrq and is_valid_ticket_number(chlrq) and JiraApi.check_chlrq_exists(chlrq):
        is_valid = True

    return is_valid


def is_valid_chlc(chlc):
    """
    Validate CHLC format and through Jira API
    """
    is_valid = False

    # Confirm chlc is valid number and is a chlc in Jira
    if chlc and is_valid_ticket_number(chlc) and JiraApi.check_chlc_exists(chlc):
        is_valid = True

    return is_valid


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
        not jira.API_EMAIL
        or not jira.API_KEY
        or not cms.EMAIL
        or not cms.PASSWORD
    ):

        return False

    return True
