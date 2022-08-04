from src.constants import colors
from .validate import (
    is_valid_chlrq,
    is_valid_chlc,
)

def get_chlrq():
    """
    Prompt user to input CHLRQ number. Validate format
    """
    # Prompt user for CHLRQ number
    chlrq = input(f'Enter {colors.OKCYAN}CHLRQ{colors.ENDC} ticket number: {colors.WHITE}')

    print(colors.ENDC, end='')

    # Check that user input chlrq is valid
    while not is_valid_chlrq(chlrq):

        # Alert user chlrq is invalid
        print(f'{colors.OKCYAN}CHLRQ-{chlrq}{colors.ENDC} is not valid. Enter 2-4 digits.')

        # Prompt user for CHLRQ number
        chlrq = input(f'{colors.ENDC}Enter {colors.OKCYAN}CHLRQ{colors.ENDC} ticket number: {colors.WHITE}')

        # Reset colors
        print(colors.ENDC, end='')

    return chlrq

def get_chlc():
    """
    Prompt user to input CHLC number. Validate format
    """
    # Prompt user for CHLC number
    chlc = input(f'Enter {colors.HEADER}CHLC{colors.ENDC} ticket number: {colors.WHITE}')

    print(colors.ENDC, end='')

    # Check that user input chlc is valid
    while not is_valid_chlc(chlc):

        # Alert user chlc is invalid
        print(f'{colors.HEADER}CHLC-{chlc}{colors.ENDC} is not valid. Enter 2-4 digits')

        # Prompt user for CHLRQ number
        chlc = input(f'Enter {colors.HEADER}CHLC{colors.ENDC} ticket number: {colors.WHITE}')

        # Reset colors
        print(colors.ENDC, end='')

    return chlc

def format_messages(messages):
    """
    Formats all messages from list into multiple lines
    """
    formatted_message = ''
    for i, message in enumerate(messages):
        if i < len(messages) - 1:
            formatted_message += message + '\n'
        else:
            formatted_message += message

    return formatted_message