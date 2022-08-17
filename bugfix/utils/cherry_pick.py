import subprocess
from bugfix.formatting import (
    Colors
)

def cherry_pick(repository_dir, branches, commit_id, debug):

    print(f'\nCherry-picking Branches...')

    # Execute command in each branch
    for i, branch in enumerate(branches):

        # Checkout to branch
        checkout_result = subprocess.check_output(f'git -C {repository_dir} checkout {branch} &>/dev/null',
                                        shell=True)
                                        # stdout=subprocess.DEVNULL,
                                        # stderr=subprocess.DEVNULL

        # print('result:', checkout_result.decode('utf-8'))

        if 'error' in checkout_result.decode('utf-8') or 'fatal' in checkout_result.decode('utf-8'):
            print('ERROR: Checkout failed')
            print(checkout_result.decode('utf-8'))

            print('\nAn error may have occured. Review the above message and determine if you should exit or continue.')
            exit_program = input('Would you like to exit? (Y/n): ')

            if exit_program.upper() == 'N':
                print('Continuing..')
            else:
                exit(1)

        # Successful checkout to branch
        else:
            # # Cherry-pick branch
            cherrypick_result = subprocess.check_output(f'git -C {repository_dir} cherry-pick {commit_id} &>/dev/null', shell=True)

            if debug:
                print(f'{Colors.FAIL}DEBUG: result=[', cherrypick_result.decode('utf-8'), ']')
            if not cherrypick_result.decode('utf-8') or 'Auto-merging' in cherrypick_result.decode('utf-8'):

                # Alert user of merge conflict
                print(f'{Colors.WARNING}[ !!! ]{Colors.ENDC} {branch}: {Colors.WARNING}MERGE CONFLICT')

                # Open VS Code to solve merge conflict
                subprocess.check_output(f'code {repository_dir}', shell=True)

                input(f'\n{Colors.ENDC}{Colors.BOLD}Press {Colors.OKGREEN}[ENTER] {Colors.ENDC}{Colors.BOLD}when changes have been made{Colors.ENDC}')

                try:
                    subprocess.call(f'git -C {repository_dir} add .',
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
                    subprocess.call(f'git -C {repository_dir} cherry-pick --continue',
                        shell=True)
                        # ,
                        # stdout=subprocess.DEVNULL,
                        # stderr=subprocess.DEVNULL)

                except:
                    # print('Caught exception!')
                    subprocess.call(f'git -C {repository_dir} commit --allow-empty',
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)

        # Inform user of successful cherry-pick, branch complete
        print(f'[{Colors.OKCYAN}{(i + 1) * 100 / len(branches):.1f}%{Colors.ENDC}]{Colors.ENDC} {branch}: {Colors.OKGREEN}[COMPLETE]{Colors.ENDC}')
