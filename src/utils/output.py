from src import constants

def print_fix_messages(fix_messages):
    for message in fix_messages:
        print(f'{constants.WHITE}\t{message}{constants.ENDC}')