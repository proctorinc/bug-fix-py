import argparse
from getpass import getpass

from src import api
from src import constants
from .validate import (
    is_valid_chlrq,
    is_valid_chlc,
)

def parse_arguments():
    """
    Parse command line arguments for program. Handle argument errors.
    """
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='bug-fix.py automates the bug-fixing process')

    # Required repository positional argument
    # parser.add_argument('-r', '--repository', type=str, help='Name of git repository to do bug-fix')

    # No push switch
    parser.add_argument('--test', action='store_true',
                    help='Enable no push mode. Does not push to git repository for testing')

    # Setup switch
    parser.add_argument('--setup', action='store_true',
                    help='Enable setup mode. Allows you to setup all environment credentials')

    # No cherrypick switch
    parser.add_argument('--no-pick', action='store_true',
                    help='Enable no cherry-pick mode. Does not cherry-pick all branches if change made on secure branch')

    # Jira transition mode switch
    parser.add_argument('--transition', action='store_true',
                    help='Enable no jira transition mode. Only transitions tickets in Jira')

    # Auto transitioning on switch
    parser.add_argument('--api', action='store_true',
                    help='Enable automatic transitioning tickets through the Jira API')

    # Auto transitioning on switch
    parser.add_argument('--debug', action='store_true',
                    help='Enable debug mode (In development)')


    # Required repository positional argument
    parser.add_argument('--chlrq', type=str, help='CHLRQ ticket number')

    # Required repository positional argument
    parser.add_argument('--chlc', type=str, help='CHLC ticket number')

    # Parse arguments
    args = parser.parse_args()

    # # If not in setup mode, require -r flag
    # if not args.setup and not args.transition and not args.repository:
    #     parser.error('-r <repository> required if not in setup mode')
    #     # parser.error('Try: bug-fix.py -r <repository_name> [--debug] [--test] [--setup] [--chlrq CHLRQ] [--chlc CHLC]')
    #     exit(1)

    return args

def get_chlrq():
    """
    Prompt user to input CHLRQ number. Validate format
    """
    # Prompt user for CHLRQ number
    chlrq = input(f'Enter {constants.OKCYAN}CHLRQ{constants.ENDC} ticket number: {constants.WHITE}')

    print(constants.ENDC, end='')

    # Check that user input chlrq is valid
    while not is_valid_chlrq(chlrq):

        # Alert user chlrq is invalid
        print(f'{constants.OKCYAN}CHLRQ-{chlrq}{constants.ENDC} is not valid. Enter 2-4 digits.')

        # Prompt user for CHLRQ number
        chlrq = input(f'{constants.ENDC}Enter {constants.OKCYAN}CHLRQ{constants.ENDC} ticket number: {constants.WHITE}')

        # Reset colors
        print(constants.ENDC, end='')

    return chlrq

def get_chlc():
    """
    Prompt user to input CHLC number. Validate format
    """
    # Prompt user for CHLC number
    chlc = input(f'Enter {constants.HEADER}CHLC{constants.ENDC} ticket number: {constants.WHITE}')

    print(constants.ENDC, end='')

    # Check that user input chlc is valid
    while not is_valid_chlc(chlc):

        # Alert user chlc is invalid
        print(f'{constants.HEADER}CHLC-{chlc}{constants.ENDC} is not valid. Enter 2-4 digits')

        # Prompt user for CHLRQ number
        chlc = input(f'Enter {constants.HEADER}CHLC{constants.ENDC} ticket number: {constants.WHITE}')

        # Reset colors
        print(constants.ENDC, end='')

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