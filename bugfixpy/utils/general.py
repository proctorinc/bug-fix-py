from typing import List


def combine_messages_into_string(messages: List[str]) -> str:
    formatted_message = ""
    for i, message in enumerate(messages):
        if message != "-":
            if i < len(messages) - 1:
                formatted_message += message + "\n"
            else:
                formatted_message += message

    return formatted_message
