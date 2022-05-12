import argparse

from api import (
    apiIsValidCredentials,
)
from constants import (
    API_EMAIL,
    API_KEY,
)
from .validation import (
    isValidCHLRQ,
    isValidCHLC,
)

from text import (
    Colors
)

def parseArguments():
    """
    Parse arguments for program. Handle argument errors.
    """
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='bug-fix.py automates the bug-fixing process')

    # Required repository positional argument
    parser.add_argument('-r', '--repository', type=str, help='Name of git repository to do bug-fix')
    
    # Debug switch
    parser.add_argument('--debug', action='store_true',
                    help='Enable debug mode. Shows output of all commands and api calls')
    
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

    # If not in setup mode, require -r flag
    if not args.setup and not args.transition and not args.repository:
        parser.error('-r <repository> required if not in setup mode')
        # parser.error('Try: bug-fix.py -r <repository_name> [--debug] [--test] [--setup] [--chlrq CHLRQ] [--chlc CHLC]')
        exit(1)

    return args

def getCHLRQ():
    """
    Prompt user to input CHLRQ number. Validate format
    """
    # Prompt user for CHLRQ number
    chlrq = input(f'Enter {Colors.OKCYAN}CHLRQ{Colors.ENDC} ticket number: {Colors.WHITE}')

    print(Colors.ENDC, end='')

    # Check that user input chlrq is valid
    while not isValidCHLRQ(chlrq):

        # Alert user chlrq is invalid
        print(f'{Colors.OKCYAN}CHLRQ-{chlrq}{Colors.ENDC} is not valid. Enter 2-4 digits.')

        # Prompt user for CHLRQ number
        chlrq = input(f'Enter {Colors.OKCYAN}CHLRQ{Colors.ENDC} ticket number: {Colors.WHITE}')

        # Reset colors
        print(Colors.ENDC, end='')

    return chlrq

def getCHLC():
    """
    Prompt user to input CHLC number. Validate format
    """
    # Prompt user for CHLC number
    chlc = input(f'Enter {Colors.HEADER}CHLC{Colors.ENDC} ticket number: {Colors.WHITE}')

    print(Colors.ENDC, end='')

    # Check that user input chlc is valid
    while not isValidCHLC(chlc):

        # Alert user chlc is invalid
        print(f'{Colors.HEADER}CHLC-{chlc}{Colors.ENDC} is not valid. Enter 2-4 digits')

        # Prompt user for CHLRQ number
        chlc = input(f'Enter {Colors.HEADER}CHLC{Colors.ENDC} ticket number: {Colors.WHITE}')

        # Reset colors
        print(Colors.ENDC, end='')

    return chlc

def setupCredentials():
    """
    Setup credentials process. Get user input to change credentials in environment
    """
    # Set Defaults
    api_email = API_EMAIL
    api_key = API_KEY

    if api_email and api_key:
        print('All credentials are setup')
        reset_credentials = input('Would you like to reset change your credentials? (y/n) ')

        if reset_credentials == 'y':
            api_email = None
            api_key = None
        else:
            exit(0)

    # If jira email does not exist, prompt for it
    while not api_email:
        api_email = input("Enter Jira Email: ")

    # If api key does not exist, prompt for it
    while not api_key:
        print('Get a Jira API key here: https://id.atlassian.com/manage-profile/security/api-tokens')
        api_key = input("Enter Jira API key: ")

    # Write to env
    with open(".env", "w") as f:
        f.write(f'API_EMAIL={api_email}\n')
        f.write(f'API_KEY={api_key}\n')

    if apiIsValidCredentials(api_email, api_key):
        print('Jira API Credentials are valid.')
        print('Run program: bug-fix.py -r <repository>')

    exit(0)

def formatMessages(messages):
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