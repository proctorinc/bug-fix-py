from typing import List
from .text import colors


def combine_messages_into_string(messages: List[str]) -> str:
    formatted_message = ""
    for i, message in enumerate(messages):
        if message != "-":
            if i < len(messages) - 1:
                formatted_message += message + "\n"
            else:
                formatted_message += message

    return formatted_message


def format_fix_messages(fix_messages: List[str]) -> str:
    formatted_message = ""
    for message in fix_messages:
        formatted_message += f"{colors.WHITE}\t{message}{colors.ENDC}"

    return formatted_message


def format_missing_credentials() -> str:
    return "missing credentials"
