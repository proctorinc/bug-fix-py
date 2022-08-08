import os
import readline
import subprocess
from typing import List, Tuple

from git import GitCommandError
from git.exc import GitError
from git.repo import Repo

from bugfixpy import utils
from bugfixpy.constants import colors, git, jira
from bugfixpy.exceptions import CheckoutFailedError, MergeConflictError
class GitRepository:
    """
    Class wrapper around GitPython for git repository functionality
    """
    __repo_name: str
    __repository: Repo
    __fix_messages: List[str]
    __did_cherrypick: bool

    def __init__(self, repo_name: str) -> None:
        self.__repo_name = repo_name
        self.__repository = self.__clone_repository()
        self.__fix_messages = []
        self.__did_cherrypick = False

    def get_num_branches(self) -> int:
        """
        Get the number of branches in this repository
        """
        return len(self.__get_filtered_branches())

    def is_full_app(self) -> bool:
        """
        Get whether the app is minified or full
        """
        branches = self.__get_filtered_branches()

        return jira.FULL_APP_SECURE_BRANCH in branches

    def get_fix_messages(self) -> List[str]:
        """
        Get fix messages created from commits to repo
        """
        return self.__fix_messages

    def did_cherrypick_run(self) -> bool:
        """
        Return whether cherrypick has been run or not
        """
        # TODO: This value needs to be modified in the cherrypick script!
        return self.__did_cherrypick

    # TODO: fix method functionality
    @staticmethod
    def did_number_of_lines_change() -> bool:
        """
        Check if the commit added or removed any lines. Return true if lines were added or removed
        """
        # added_or_removed_lines = False

        # diff = repository.git.diff('--numstat', 'HEAD^').split("\n")

        # for edited_file_stat in diff:
        #     stat = edited_file_stat.split()

        #     if stat[0] == '-':
        #         added = 0
        #     else:
        #         added = int(stat[0])

        #     if stat[1] == '-':
        #         removed = 0
        #     else:
        #         removed = stat[1]

        #     if added - removed != 0:
        #         added_or_removed_lines = True

        # return added_or_removed_lines
        return True

    def push(self) -> None:
        """
        Push repository changes to github
        """
        # Push commit to the repository
        subprocess.check_output(
            f"git -C {self.__get_repository_dir()} push --all", shell=True
        )

    def __checkout_to_branch(self, branch:str) -> None:
        """
        Checkout to a branch in the git repository
        """
        result = subprocess.check_output(
            f"git -C {self.__get_repository_dir()} checkout {branch} &>/dev/null", shell=True
        ).decode("utf-8")

        errors = ["error", "fatal"]

        # Check if error exists in result
        if any(error in errors for error in result):
            print('Checkout Failed - Determine if you want to continue')
            # TODO: throw fatal checkout error

    def __add_changes_to_branch(self) -> None:
        """
        Add all current changes to commit
        """
        subprocess.call(
            f"git -C {self.__get_repository_dir()} add .",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def __continue_cherrypicking_branch(self) -> None:
        """
        Run git command to continue cherrypicking
        """
        subprocess.call(
            f"git -C {self.__get_repository_dir()} cherry-pick --continue", shell=True
        )

    def __commit_changes_allow_empty(self) -> None:
        """
        Commit changes with empty commit message
        """
        subprocess.call(
            f"git -C {self.__get_repository_dir()} commit --allow-empty",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def __cherrypick_branch(self, commit_id) -> None:
        """
        Cherrypick commit id in current branch
        """
        # Cherry-pick branch
        result = subprocess.check_output(
            f"git -C {self.__get_repository_dir()} cherry-pick {commit_id} &>/dev/null",
            shell=True,
        ).decode("utf-8")

        if not result or "Auto-merging":
            raise MergeConflictError("Merge conflict occurred")

    def __get_repository_dir(self) -> str:
        """
        Returns absolute url for repository folder
        """
        return os.path.join(git.REPO_DIR, self.__repo_name)

    def __clone_repository(self) -> Repo:
        """
        Clone repository and return valid instance. Handle errors for invalid repository
        """
        git_url = f"{jira.SCW_GIT_URL}/{self.__repo_name}.git"
        repository_dir = self.__get_repository_dir()

        # If repo folder already exists, remove it
        if os.path.isdir(repository_dir):

            # Delete repository
            subprocess.check_output(f"sudo rm -r {repository_dir}", shell=True)
        try:
            # Clone repository
            Repo.clone_from(git_url, repository_dir)

        except GitError as err:
            raise GitError(
                f"{colors.FAIL}Either '{self.__repo_name}' is not a valid repository\nor you do not have the correct rights to access this repo{colors.ENDC}"
            ) from err

        # Create repository object
        repo = Repo(repository_dir)

        return repo

    def __get_filtered_branches(self) -> List[str]:
        """
        Parse branches from remote refs and remove unwanted branches
        """
        remote_refs = self.__repository.remote().refs
        filtered_branches = []

        # Loop over remote references
        for refs in remote_refs:

            # Remove origin/ from branch name
            branch = str(refs.name.split("origin/", 1)[1])

            # Filter branches
            if branch not in jira.IGNORE_BRANCHES:
                filtered_branches.append(branch)

        return filtered_branches

    def __get_last_commit_id(self) -> str:
        """
        Returns commit id of last commit
        """
        return str(self.__repository.rev_parse("HEAD"))

    def run_bug_fix(self) -> None:
        """
        Run bug fix. Loop over branches to fix. After fixing, prompt
        user if they want to fix another
        """
        branches = self.__get_filtered_branches()
        is_full_app = self.is_full_app()

        # Default user is not done fixing branches
        done_fixing = False

        # Hold fix messages for all branches in list
        fix_messages = []

        # Continue to fix branches until user is done
        while not done_fixing:

            ###########
            #
            # Allow user to stop fixing branch at anytime
            #
            ###########

            # Fix the branch and retrieve the name and fix explanation
            fix_message, fixed_branch = self.fix_and_commit_branch(
                self.__repository,
                self.__get_repository_dir(),
                branches,
                is_full_app,
            )

            # Remove initial_branch from branches to avoid cherry-picking it
            branches.remove(fixed_branch)

            # Add message to list of messages
            fix_messages.append(fix_message)

            # If full app and fix was on the secure branch, cherry-pick branches
            if is_full_app and fixed_branch == jira.FULL_APP_SECURE_BRANCH:

                # Get the commit ID
                commit_id = self.__get_last_commit_id()

                print("\nCherry-picking Branches...")
                # Run cherry-pick method
                self.cherrypick_commit_across_all_branches(commit_id)

                # Confirm that cherrypick occurred
                self.__did_cherrypick = True

            # Prompt user to fix another branch
            fix_branch = input(
                f"\nFix another branch? (y/{colors.BOLD}{colors.WHITE}N{colors.ENDC}){colors.ENDC}: {colors.WHITE}"
            )

            print(colors.ENDC, end="")

            # If not yes, user is done fixing
            if fix_branch != "y":
                done_fixing = True

    def cherrypick_commit_across_all_branches(self, commit_id) -> None:
        """
        Cherrypick git repository
        """
        branches = self.__get_filtered_branches()

        # Cherrypick each branch
        for i, branch in enumerate(branches):

            # Attempt to checkout to branch
            try:
                self.__checkout_to_branch(branch)

            # If checkout failed
            except CheckoutFailedError as err:
                print("Exception occurred while checking out to branch")
                print(err)
                utils.prompt_user_to_exit_or_continue()

            # Successful checkout to branch
            else:
                # Attempt to cherrypick branch
                try:
                    self.__cherrypick_branch(commit_id)

                # Check if merge conflict occurred
                except MergeConflictError:
                    utils.warn_user_of_merge_conflict(branch)

                    self.open_repository_in_vscode()

                    utils.prompt_user_to_resolve_merge_conflict()

                    # Attempt to add changes and continue cherrypick
                    try:
                        self.__add_changes_to_branch()
                        self.__continue_cherrypicking_branch()

                    # Create empty commit if error occurs
                    # TODO: figure out what exception is being thrown here
                    except Exception as err:
                        print("Exception occurred while adding and continuing cherrypick")
                        print(err)
                        print(type(err))
                        self.__commit_changes_allow_empty()

            # Inform user of successful cherry-pick, branch complete
            print(
                f"[{colors.OKCYAN}{(i + 1) * 100 / len(branches):.1f}%{colors.ENDC}]{colors.ENDC} {branch}: {colors.OKGREEN}[COMPLETE]{colors.ENDC}"
            )

    def open_repository_in_vscode(self):
        """ Opens repository code in VS Code """
        subprocess.check_output(f"code {self.__get_repository_dir()}", shell=True)

    def fix_and_commit_branch(self,
        repository, repository_dir, branches, is_full_app
    ) -> Tuple[str, str]:
        """
        Checks the user out to a branch of their choice, making sure it is a valid branch.
        Opens VS Code for user to make the fix and prompts user to press ENTER when done.
        Continues process if changes were made successfully and commits with a message.
        Returns the commit message and the branch the user successfully fixed.
        """
        # Default commit to unsuccessful
        successful_commit = False

        # Default fix message to blank
        fix_message = ""

        # Enable tab completion
        readline.parse_and_bind("tab: complete")

        # Set completion to list of branches
        readline.set_completer(utils.Completer().get_list_completer(branches))

        # Prompt user for branch where the fix will be made
        initial_branch = input(f"\nEnter name of branch to fix: {colors.WHITE}")

        print(colors.ENDC, end="")

        # Check that user input is a valid branch
        while initial_branch not in branches:

            # Alert user branch name is invalid
            print(
                f'{colors.FAIL}"{initial_branch}" is not a valid branch name{colors.ENDC}'
            )

            # Check if user entered "secure" on a minified app. Suggest minified secure branch
            if (not is_full_app) and initial_branch == jira.FULL_APP_SECURE_BRANCH:
                minified_secure_branches = self.get_minified_secure_branch()
                print(
                    f"\nThis app is {colors.OKCYAN}Minified{colors.ENDC}, enter the correct secure branch: {colors.HEADER}"
                )
                for branch in minified_secure_branches:
                    print(branch, end=" ")
                print(colors.ENDC)

            # Prompt user for branch again
            initial_branch = input(f"Enter name of branch to fix: {colors.WHITE}")

            print(colors.ENDC, end="")

        # Disable tab completion
        readline.parse_and_bind("tab: self-insert")

        # Checkout to branch
        repository.git.checkout(initial_branch)

        # Prompt user to make fix
        print(
            f"{colors.UNDERLINE}{colors.OKGREEN}{colors.BOLD}\nMake the fix in VS Code{colors.ENDC}"
        )

        # Open VS Code to make fix
        subprocess.check_output(f"code {repository_dir}", shell=True)

        # Continue until fix message is entered
        while not fix_message:
            # Prompt user to input fix message
            fix_message = input(f"Enter description of fix: {colors.WHITE}")

            print(colors.ENDC, end="")

        # Continue until a valid commit is successful
        while not successful_commit:
            try:
                # Add files for commit
                repository.git.add(u=True)

                # Commit changes in branch with message
                repository.git.commit("-m", fix_message)

            except GitCommandError:
                # if debug:
                #     print(f'{colors.FAIL}DEBUG: error=[{e}]')
                # Alert user that no change has been made
                print(
                    f"{colors.ENDC}{colors.FAIL}No Changes have been made, please make a fix before continuing"
                )
                print(
                    f"Press {colors.UNDERLINE}ctrl+s{colors.ENDC}{colors.FAIL} to confirm changes"
                )

                # Prompt user to press enter when fix is made
                input(
                    f"{colors.UNDERLINE}{colors.OKGREEN}{colors.BOLD}\nPress [Enter] after fix{colors.ENDC}"
                )

            else:
                successful_commit = True

        return fix_message, initial_branch

    def get_minified_secure_branch(self) -> List[str]:
        """
        Gets the secure branch of a minified app. Minified app's secure branch starts with 'secure'
        """
        secure_branches = []

        for branch in self.__get_filtered_branches():

            # Check if branch starts with 'secure'
            if jira.FULL_APP_SECURE_BRANCH in branch:
                secure_branches.append(branch)

        return secure_branches
