import re
from bugfixpy.jira import api
from bugfixpy.constants import cms, jira


def is_valid_ticket_number(ticket) -> bool:
    """
    Validate ticket number input format
    """
    return bool(len(ticket) < 5 and len(ticket) > 1 and ticket.isdigit())


def is_valid_challenge_request_issue(chlrq) -> bool:
    """
    Validate CHLRQ format and through Jira API
    """
    is_valid = False

    # Confirm chlrq is valid number and is a chlrq in Jira
    if chlrq and is_valid_ticket_number(chlrq) and api.check_chlrq_exists(chlrq):
        is_valid = True

    return is_valid


def is_valid_chlc(chlc):
    """
    Validate CHLC format and through Jira API
    """
    is_valid = False

    # Confirm chlc is valid number and is a chlc in Jira
    if chlc and is_valid_ticket_number(chlc) and api.check_chlc_exists(chlc):
        is_valid = True

    return is_valid


# TODO: finish method
def is_valid_challenge_id(cid) -> bool:
    """
    Check whether the challenge id is valid or not
    """
    # Regex string checks for 24 character string made up of lower case characters and digits
    return bool(re.match("^([a-z0-9]{24})", cid))


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


def has_valid_credentials() -> bool:
    if not jira.API_EMAIL or not jira.API_KEY or not cms.EMAIL or not cms.PASSWORD:
        return False

    response_code = api.get_response_code_from_query_to_verify_credentials()

    if response_code != 200:
        print("Invalid API credentials: Invalid email or permissions on account")
        print("confirm your credentials are correct")
        print("run bug-fix.py --setup to change credentials")
        return False

    return True
