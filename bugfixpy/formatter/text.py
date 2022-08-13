"""
Text class formats colors for text output to console
"""


from typing import List
from bugfixpy.constants import colors


class Text:
    """
    Text class
    """

    def __init__(self, *args):
        """
        Text class overloaded constructor. Choice of text and the color to
        format that text, or similar with unformatted text beforehand.
        """
        if len(args) == 2:
            text = str(args[0])
            color_fmt = str(args[1])
            self.__validate_color(color_fmt)
            self.__value = f"{color_fmt}{text}{colors.ENDC}"

        elif len(args) == 3:
            pre_text = str(args[0])
            text = str(args[1])
            color_fmt = str(args[2])
            self.__validate_color(color_fmt)
            self.__value = f"{pre_text} {color_fmt}{text}{colors.ENDC}"
        else:
            raise TypeError(f"Incorrect number of arguments: {len(args)}")

    def display(self):
        """
        Prints out the formatted text
        """
        print(self)

    def prompt(self):
        """
        Use text as prompt for user input
        """
        return input(str(self))

    def __validate_color(self, color_fmt: str):
        """
        Validates that the input color format is a valid color constant
        """
        if color_fmt not in colors.ALL:
            raise ValueError(f"Color {color_fmt} is not a valid color")

    def __str__(self):
        """
        Overrides string output with returning the value of color formatted text
        """
        return self.__value


def format_fix_messages(fix_messages: List[str]) -> str:
    """
    Print fix message
    """
    formatted_message = ""
    for message in fix_messages:
        formatted_message += f"{colors.WHITE}\t{message}{colors.ENDC}"

    return formatted_message


def format_missing_credentials() -> str:
    """Print missing credentials"""
    return "missing credentials"
    # Text('Credentials not setup. Run \'bug-fix.py --setup\' to set up environment variables', colors.FAIL).display()

    # # Notify that no email is present
    # if not constants.JIRA_API_EMAIL:
    #     Text('No API email present', colors.FAIL).display()

    # # Notify that no api key is present
    # if not constants.JIRA_API_KEY:
    #     Text('No API key present', colors.FAIL).display()

    # # Notify that no email is present
    # if not constants.CMS_EMAIL:
    #     Text('No CMS email present', colors.FAIL).display()

    # # Notify that no api key is present
    # if not constants.CMS_PASSWORD:
    #     Text('No CMS password present', colors.FAIL).display()
