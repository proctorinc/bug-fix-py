import subprocess

from bugfixpy.exceptions import CheckoutFailedError, MergeConflictError
from bugfixpy.utils import prompt_user
from bugfixpy.git import Repository
from bugfixpy.constants import colors


# def cherrypick_commit_across_all_branches(repository: Repository, commit_id) -> None:
#     """
#     Cherrypick git repository
#     """
#     branches = repository.get_filtered_branches()

#     # Cherrypick each branch
#     for i, branch in enumerate(branches):

#         # Attempt to checkout to branch
#         try:
#             repository.checkout_to_branch(branch)

#         # If checkout failed
#         except CheckoutFailedError as err:
#             print("Exception occurred while checking out to branch")
#             print(err)
#             user_input.if_they_want_to_continue()

#         # Successful checkout to branch
#         else:
#             # Attempt to cherrypick branch
#             try:
#                 repository.cherrypick_branch(commit_id)

#             # Check if merge conflict occurred
#             except MergeConflictError:
#                 # print(instructions.WARN_USER_OF_MERGE_CONFLICT.format(branch=branch))
#                 print(f"{colors.WARNING}[ !!! ]{colors.ENDC} {branch}: {colors.WARNING}MERGE CONFLICT")
#                 repository.open_code_in_editor()
#                 user_input.to_resolve_merge_conflict()

#                 # Attempt to add changes and continue cherrypick
#                 try:
#                     repository.add_changes_to_branch()
#                     repository.continue_cherrypicking_branch()

#                 # Create empty commit if error occurs
#                 # TODO: figure out what exception is being thrown here
#                 except Exception as err:
#                     print("Exception occurred while adding and continuing cherrypick")
#                     print(err)
#                     print(type(err))
#                     repository.commit_changes_allow_empty()

#         # Inform user of successful cherry-pick, branch complete
#         print(
#             f"[{colors.OKCYAN}{(i + 1) * 100 / len(branches):.1f}%{colors.ENDC}]{colors.ENDC}"
#             f" {branch}: {colors.OKGREEN}[COMPLETE]{colors.ENDC}"
#         )


# def cherry_pick(repository_dir, branches, commit_id, debug):
def cherrypick_commit_across_all_branches(repository: Repository, commit_id) -> None:

    debug = False
    repository_dir = repository.get_repository_dir()
    branches = repository.get_filtered_branches()

    print(f"\nCherry-picking Branches...")

    # Execute command in each branch
    for i, branch in enumerate(branches):

        # Checkout to branch
        checkout_result = subprocess.check_output(
            f"git -C {repository_dir} checkout {branch} &>/dev/null", shell=True
        )

        if debug:
            print(
                f"{colors.FAIL}DEBUG: checkout_result=["
                + checkout_result.decode("utf-8")
                + f"]{colors.ENDC}"
            )
        if "error" in checkout_result.decode(
            "utf-8"
        ) or "fatal" in checkout_result.decode("utf-8"):
            print("ERROR: Checkout failed")
            print(checkout_result.decode("utf-8"))

            print(
                "\nAn error may have occured. Review the above message and determine if you should exit or continue."
            )
            exit_program = input("Would you like to exit? (Y/n): ")

            if exit_program.upper() == "N":
                print("Continuing..")
            else:
                exit(1)

        # Successful checkout to branch
        else:
            # # Cherry-pick branch
            cherrypick_result = subprocess.check_output(
                f"git -C {repository_dir} cherry-pick {commit_id} &>/dev/null",
                shell=True,
            )

            if debug:
                print(
                    f"{colors.FAIL}DEBUG: result=[",
                    cherrypick_result.decode("utf-8"),
                    f"]{colors.ENDC}",
                )
            if not cherrypick_result.decode(
                "utf-8"
            ) or "CONFLICT" in cherrypick_result.decode(
                "utf-8"
            ):  # or 'Auto-merging' in cherrypick_result.decode('utf-8')

                # Alert user of merge conflict
                print(
                    f"{colors.WARNING}[ !!! ]{colors.ENDC} {branch}: {colors.WARNING}MERGE CONFLICT"
                )

                # Open VS Code to solve merge conflict
                subprocess.check_output(f"code {repository_dir}", shell=True)

                input(
                    f"\n{colors.ENDC}{colors.BOLD}Press {colors.OKGREEN}[ENTER] {colors.ENDC}{colors.BOLD}when changes have been made{colors.ENDC}"
                )

                try:
                    if debug:
                        print(f"{colors.FAIL}DEBUG: running add .{colors.ENDC}")
                    subprocess.call(
                        f"git -C {repository_dir} add .",
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    if debug:
                        print(
                            f"{colors.FAIL}DEBUG: running cherry-pick --continue{colors.ENDC}"
                        )
                    subprocess.call(
                        f"git -C {repository_dir} cherry-pick --continue", shell=True
                    )

                except:
                    if debug:
                        print(f"{colors.FAIL}DEBUG: Caught exception!")
                    subprocess.call(
                        f"git -C {repository_dir} commit --allow-empty",
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )

        # Inform user of successful cherry-pick, branch complete
        print(
            f"[{colors.OKCYAN}{(i + 1) * 100 / len(branches):.1f}%{colors.ENDC}]{colors.ENDC} {branch}: {colors.OKGREEN}[COMPLETE]{colors.ENDC}"
        )
