import sys
import readline
from typing import Callable, List

from bugfixpy.exceptions import InvalidIssueIdError
from bugfixpy.constants import colors, jira
from bugfixpy.git.repository import Repository
from bugfixpy.utils import validate
from bugfixpy.formatter import completer
from bugfixpy.jira.issue import (
    ApplicationCreationIssue,
    ChallengeCreationIssue,
    ChallengeRequestIssue,
)


def __get_valid_input(
    prompt: str, invalid_message: str, is_valid: Callable[[str], bool]
) -> str:
    value = input(prompt)
    print(colors.ENDC, end="")

    while not is_valid(value):
        print(f"{colors.FAIL}{invalid_message}{value}{colors.ENDC}")
        value = input(prompt)
        print(colors.ENDC, end="")

    return value


def get_challenge_request_issue() -> ChallengeRequestIssue:
    challenge_request = None

    while not challenge_request:
        challenge_id = input(
            f"Enter {colors.OKCYAN}CHLRQ{colors.ENDC} ticket number: {colors.WHITE}"
        )

        try:
            challenge_request = ChallengeRequestIssue(challenge_id)

        except InvalidIssueIdError:
            print(
                f"{colors.OKCYAN}CHLRQ-{challenge_id}{colors.ENDC} is not valid. Enter 2-4 digits."
            )
    return challenge_request


def get_challenge_creation_issue() -> ChallengeCreationIssue:
    challenge_creation = None

    while not challenge_creation:
        challenge_id = input(
            f"Enter {colors.OKCYAN}CHLC{colors.ENDC} ticket number: {colors.WHITE}"
        )

        try:
            challenge_creation = ChallengeCreationIssue(challenge_id)

        except InvalidIssueIdError:
            print(
                f"{colors.OKCYAN}CHLC-{challenge_id}{colors.ENDC} is not valid. Enter 2-4 digits."
            )
    return challenge_creation


def get_application_creation_issue() -> ApplicationCreationIssue:
    application_creation = None

    while not application_creation:
        challenge_id = input(
            f"Enter {colors.OKCYAN}CHLC{colors.ENDC} ticket number: {colors.WHITE}"
        )

        try:
            application_creation = ApplicationCreationIssue(challenge_id)

        except InvalidIssueIdError:
            print(
                f"{colors.OKCYAN}CHLC-{challenge_id}{colors.ENDC} is not valid. Enter 2-4 digits."
            )
    return application_creation


def format_messages(messages: List[str]) -> str:
    """
    Formats all messages from list into multiple lines
    """
    formatted_message = ""
    for i, message in enumerate(messages):
        if message != "-":
            if i < len(messages) - 1:
                formatted_message += message + "\n"
            else:
                formatted_message += message

    return formatted_message


def prompt_user_to_resolve_merge_conflict() -> None:
    """
    Prompt user to resolve merge conflict
    """
    input(
        f"\n{colors.ENDC}{colors.BOLD}Press {colors.OKGREEN}[ENTER] {colors.ENDC}{colors.BOLD}when"
        f" changes have been made{colors.ENDC}"
    )


def prompt_user_to_exit_or_continue() -> None:
    """
    Prompt user to exit of continue
    """
    # Prompt user to exit program
    exit_program = input("Would you like to exit? (Y/n): ")

    if exit_program.upper() == "N":
        print("Continuing..")
    else:
        sys.exit(1)


def get_challenge_id() -> str:
    """
    Get challenge ID from user
    """
    prompt = "Enter Challenge ID: "
    invalid_message = "'{value}' is not a valid Challenge ID"

    challenge_id = __get_valid_input(
        prompt, invalid_message, validate.is_valid_challenge_id
    )

    return challenge_id


def get_next_branch(repository: Repository) -> str:
    """
    Prompts user for next branch to checkout to
    """
    branches = repository.get_filtered_branches()
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer.get_list_completer(branches))

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
                f"\nThis app is {colors.OKCYAN}Minified{colors.ENDC}, enter the correct secure"
                f" branch: {colors.HEADER}"
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


def get_next_branch_or_continue(repository: Repository) -> str:
    """
    Prompts user for next branch to checkout to
    """
    branches = repository.get_filtered_branches()
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer.get_list_completer(branches))

    branch = input(
        f"\nEnter name of branch to fix another {colors.WHITE}(continue){colors.ENDC}: {colors.WHITE}"
    )

    print(colors.ENDC, end="")

    if branch == "":
        return ""

    # Check that user input is a valid branch
    while branch not in branches:

        # Alert user branch name is invalid
        print(f'{colors.FAIL}"{branch}" is not a valid branch name{colors.ENDC}')

        # Check if user entered "secure" on a minified app. Suggest minified secure branch
        if (not repository.is_full_app) and branch == jira.FULL_APP_SECURE_BRANCH:
            minified_secure_branches = repository.get_minified_secure_branch()
            print(
                f"\nThis app is {colors.OKCYAN}Minified{colors.ENDC}, enter the correct secure"
                f" branch: {colors.HEADER}"
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
    prompt = f"Enter description of fix: {colors.WHITE}"

    fix_message = __get_valid_input(prompt, "", validate.is_valid_fix_message)

    if fix_message == " ":
        fix_message = "-"

    return fix_message


def prompt_want_to_continue() -> bool:
    """
    Return true if the user wants to continue, otherwise return false
    """
    will_continue = input(
        f"\nFix another branch? (y/{colors.BOLD}{colors.WHITE}N{colors.ENDC}){colors.ENDC}:"
        f" {colors.WHITE}"
    )
    return will_continue.upper() != "Y"


def prompt_user_to_press_enter() -> None:
    """
    Prompts user to press enter, blocks until enter is pressed
    """
    input(
        f"{colors.UNDERLINE}{colors.OKGREEN}{colors.BOLD}\nPress [Enter] after fix{colors.ENDC}"
    )


def get_repository_name() -> str:
    """
    Gets the name of the git repository
    """
    prompt = "Enter repo name: "
    invalid_message = "'{value}' is not a valid Git repository"

    repo_name = __get_valid_input(
        prompt, invalid_message, validate.is_valid_repository_name
    )

    return repo_name
