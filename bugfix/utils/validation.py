from api import (
    apiConfirmCHLRQ,
    apiConfirmCHLC,
)

def isValidTicketNumber(ticket):
    """
    Validate ticket number input format
    """
    return len(ticket) < 5 and len(ticket) > 1 and ticket.isdigit()

def isValidCHLRQ(chlrq):
    """
    Validate CHLRQ format and through Jira API
    """
    isValid = False

    # Confirm chlrq is valid number and is a chlrq in Jira
    if chlrq and isValidTicketNumber(chlrq) and apiConfirmCHLRQ(chlrq):
        isValid = True

    return isValid

def isValidCHLC(chlc):
    """
    Validate CHLC format and through Jira API
    """
    isValid = False

    # Confirm chlc is valid number and is a chlc in Jira
    if chlc and isValidTicketNumber(chlc) and apiConfirmCHLC(chlc):
        isValid = True

    return isValid