class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[1;37m'

class Completer:
    """
    Class to enable tab completions for a list
    """
    def get_list_completer(self, list):
        """
        Creates and returns a completer for a list of strings
        """
        def completer(text, state):
            """
            Returns a list of strings that match the current state
            """
            options = [i for i in list if i.startswith(text)]
            if state < len(options):
                return options[state]
            else:
                return None

        return completer