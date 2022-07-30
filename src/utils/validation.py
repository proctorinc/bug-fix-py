from src import api

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