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