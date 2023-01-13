from typing import Callable, List, Optional


def get_list_completer(
    completer_list: List[str],
) -> Callable[[str, int], Optional[str]]:
    def completer(text: str, state: int) -> Optional[str]:
        options = [i for i in completer_list if i.startswith(text)]
        if state < len(options):
            return options[state]

        return None

    return completer
