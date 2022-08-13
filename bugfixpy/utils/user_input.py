import readline
from typing import List
from bugfixpy.constants import colors, jira
from bugfixpy.gitrepository import GitRepository
from bugfixpy.utils import validate
from bugfixpy.formatter import completer


def get_chlrq():
    """
    Prompt user to input CHLRQ number. Validate format
    """
    # Prompt user for CHLRQ number
    chlrq = input(
        f"Enter {colors.OKCYAN}CHLRQ{colors.ENDC} ticket number: {colors.WHITE}"
    )

    print(colors.ENDC, end="")

    # Check that user input chlrq is valid
    while not validate.is_valid_chlrq(chlrq):

        # Alert user chlrq is invalid
        print(
            f"{colors.OKCYAN}CHLRQ-{chlrq}{colors.ENDC} is not valid. Enter 2-4 digits."
        )

        # Prompt user for CHLRQ number
        chlrq = input(
            f"{colors.ENDC}Enter {colors.OKCYAN}CHLRQ{colors.ENDC} ticket number: {colors.WHITE}"
        )

        # Reset colors
        print(colors.ENDC, end="")

    return chlrq


def get_chlc():
    """
    Prompt user to input CHLC number. Validate format
    """
    # Prompt user for CHLC number
    chlc = input(
        f"Enter {colors.HEADER}CHLC{colors.ENDC} ticket number: {colors.WHITE}"
    )

    print(colors.ENDC, end="")

    # Check that user input chlc is valid
    while not validate.is_valid_chlc(chlc):

        # Alert user chlc is invalid
        print(f"{colors.HEADER}CHLC-{chlc}{colors.ENDC} is not valid. Enter 2-4 digits")

        # Prompt user for CHLRQ number
        chlc = input(
            f"Enter {colors.HEADER}CHLC{colors.ENDC} ticket number: {colors.WHITE}"
        )

        # Reset colors
        print(colors.ENDC, end="")

    return chlc


def format_messages(messages):
    """
    Formats all messages from list into multiple lines
    """
    formatted_message = ""
    for i, message in enumerate(messages):
        if i < len(messages) - 1:
            formatted_message += message + "\n"
        else:
            formatted_message += message

    return formatted_message


def prompt_user_to_resolve_merge_conflict():
    """
    Prompt user to resolve merge conflict
    """
    input(
        f"\n{colors.ENDC}{colors.BOLD}Press {colors.OKGREEN}[ENTER] {colors.ENDC}{colors.BOLD}when changes have been made{colors.ENDC}"
    )


def prompt_user_to_exit_or_continue():
    """
    Prompt user to exit of continue
    """
    # Prompt user to exit program
    exit_program = input("Would you like to exit? (Y/n): ")

    if exit_program.upper() == "N":
        print("Continuing..")
    else:
        exit(1)


def get_challenge_id() -> str:
    """
    Get challenge ID from user
    """
    not_done = True
    challenge_id = ""
    while not_done:
        challenge_id = input("Enter Challenge ID: ")

        if not validate.is_valid_challenge_id(challenge_id):
            print(f"'{challenge_id}' is not a valid Challenge ID")
        else:
            not_done = False

    return challenge_id


def get_next_branch(branches: List[str], repository: GitRepository) -> str:
    """
    Prompts user for next branch to checkout to
    """
    # Enable tab completion
    readline.parse_and_bind("tab: complete")

    # Set completion to list of branches
    readline.set_completer(completer.get_list_completer(branches))

    # Prompt user for branch where the fix will be made
    branch = input(f"\nEnter name of branch to fix: {colors.WHITE}")

    print(colors.ENDC, end="")

    # Check that user input is a valid branch
    while branch not in branches:

        # Alert user branch name is invalid
        print(f'{colors.FAIL}"{branch}" is not a valid branch name{colors.ENDC}')

        # Check if user entered "secure" on a minified app. Suggest minified secure branch
        if (not repository.is_full_app) and branch == jira.FULL_APP_SECURE_BRANCH:
            minified_secure_branches = repository.get_minified_secure_branch()
            print(
                f"\nThis app is {colors.OKCYAN}Minified{colors.ENDC}, enter the correct secure branch: {colors.HEADER}"
            )
            for branch in minified_secure_branches:
                print(branch, end=" ")
            print(colors.ENDC)

        # Prompt user for branch again
        branch = input(f"Enter name of branch to fix: {colors.WHITE}")

        print(colors.ENDC, end="")

    # Disable tab completion
    readline.parse_and_bind("tab: repository-insert")

    return branch


def get_fix_message() -> str:
    """
    Prompts user for description of fix that was made. Fix message cannot be blank
    """
    # Default fix message to blank
    fix_message = ""

    # Continue until fix message is entered
    while not fix_message:

        # Prompt user to input fix message
        fix_message = input(f"Enter description of fix: {colors.WHITE}")

        print(colors.ENDC, end="")

    return fix_message


def prompt_want_to_continue() -> bool:
    """
    Return true if the user wants to continue, otherwise return false
    """
    will_continue = input(
        f"\nFix another branch? (y/{colors.BOLD}{colors.WHITE}N{colors.ENDC}){colors.ENDC}: {colors.WHITE}"
    )
    return will_continue.upper() != "Y"


def prompt_user_to_press_enter() -> None:
    """
    Prompts user to press enter, blocks until enter is pressed
    """
    input(
        f"{colors.UNDERLINE}{colors.OKGREEN}{colors.BOLD}\nPress [Enter] after fix{colors.ENDC}"
    )
