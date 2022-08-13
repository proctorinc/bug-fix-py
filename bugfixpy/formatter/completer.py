"""
Completer module adds autocomplete to user input based off of an input list of choices
"""


from typing import Callable, List, Optional


def get_list_completer(
    completer_list: List[str],
) -> Callable[[str, int], Optional[str]]:
    """
    Creates and returns a completer for a list of strings
    """

    def completer(text: str, state: int) -> Optional[str]:
        """
        Returns a list of strings that match the current state of the user input
        """
        options = [i for i in completer_list if i.startswith(text)]
        if state < len(options):
            return options[state]

        return None

    return completer
