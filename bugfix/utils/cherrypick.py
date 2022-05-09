import subprocess
from xml.dom.expatbuilder import parseString
import git
import traceback
from text import (
    Colors
)

def cherrypick(repository_url, branches, commit_id):

    print(f'\nCherry-picking Branches...')

    # Execute command in each branch
    for i, branch in enumerate(branches):

        # Checkout to branch
        checkout_result = subprocess.check_output(f'git -C {repository_url} checkout {branch} &>/dev/null',
                                        shell=True)
                                        # stdout=subprocess.DEVNULL,
                                        # stderr=subprocess.DEVNULL

        # print('result:', checkout_result.decode('utf-8'))

        if 'error' in checkout_result.decode('utf-8') or 'fatal' in checkout_result.decode('utf-8'):
            print('ERROR: Checkout failed')
            exit(1)

        # Successful checkout to branch
        else:
            # # Cherry-pick branch
            cherrypick_result = subprocess.check_output(f'git -C {repository_url} cherry-pick {commit_id} &>/dev/null', shell=True)

            if not cherrypick_result.decode('utf-8'):

                # Alert user of merge conflict
                print(f'{Colors.WARNING}[ !!! ]{Colors.ENDC} {branch}: {Colors.WARNING}MERGE CONFLICT')

                # Open VS Code to solve merge conflict
                subprocess.check_output(f'code {repository_url}', shell=True)

                input(f'\n{Colors.ENDC}{Colors.BOLD}Press {Colors.OKGREEN}[ENTER] {Colors.ENDC}{Colors.BOLD}when changes have been made{Colors.ENDC}')

                try:
                    subprocess.call(f'git -C {repository_url} add .',
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
                    subprocess.call(f'git -C {repository_url} cherry-pick --continue',
                        shell=True)
                        # ,
                        # stdout=subprocess.DEVNULL,
                        # stderr=subprocess.DEVNULL)

                except:
                    # print('Caught exception!')
                    subprocess.call(f'git -C {repository_url} commit --allow-empty',
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)

        # Inform user of successful cherry-pick, branch complete
        print(f'[{Colors.OKCYAN}{(i + 1) * 100 / len(branches):.1f}%{Colors.ENDC}]{Colors.ENDC} {branch}: {Colors.OKGREEN}[COMPLETE]{Colors.ENDC}')
