"""
Git Repository class for running git actions on SCW content repositories
"""


import os
from typing import List
import subprocess

from git.repo import Repo

from bugfixpy.utils import output, user_input
from bugfixpy.constants import colors, git, jira
from bugfixpy.exceptions import CheckoutFailedError, MergeConflictError


class GitRepository:
    """
    Wrapper class around GitPython library for git repository functionality
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
        return len(self.get_filtered_branches())

    def is_full_app(self) -> bool:
        """
        Get whether the app is minified or full
        """
        branches = self.get_filtered_branches()

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

    def set_cherrypick_ran(self) -> None:
        """
        Set whether the repository was cherrypicked to True
        """
        self.__did_cherrypick = True

    # TODO: fix method functionality
    def did_number_of_lines_change(self) -> bool:
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

    def push_fix_to_github(self) -> None:
        """
        Push repository changes to github
        """
        # Push commit to the repository
        subprocess.check_output(
            f"git -C {self.get_repository_dir()} push --all", shell=True
        )

    def checkout_to_branch(self, branch: str) -> None:
        """
        Checkout to a branch in the git repository
        """
        result = subprocess.check_output(
            f"git -C {self.get_repository_dir()} checkout {branch} &>/dev/null",
            shell=True,
        ).decode("utf-8")

        errors = ["error", "fatal"]

        # Check if error exists in result
        if any(error in errors for error in result):
            print("Checkout Failed - Determine if you want to continue")
            # TODO: throw fatal checkout error

    def add_changes_to_branch(self) -> None:
        """
        Add all current changes to commit
        """
        subprocess.call(
            f"git -C {self.get_repository_dir()} add .",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def __continue_cherrypicking_branch(self) -> None:
        """
        Run git command to continue cherrypicking
        """
        subprocess.call(
            f"git -C {self.get_repository_dir()} cherry-pick --continue", shell=True
        )

    def commit_changes_with_message(self, message) -> None:
        """
        Commit changes with a message
        """
        self.__repository.git.commit("-m", message)

    def __commit_changes_allow_empty(self) -> None:
        """
        Commit changes with empty commit message
        """
        subprocess.call(
            f"git -C {self.get_repository_dir()} commit --allow-empty",
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
            f"git -C {self.get_repository_dir()} cherry-pick {commit_id} &>/dev/null",
            shell=True,
        ).decode("utf-8")

        if not result or "Auto-merging":
            raise MergeConflictError("Merge conflict occurred")

    def get_repository_dir(self) -> str:
        """
        Returns absolute url for repository folder
        """
        return os.path.join(git.REPO_DIR, self.__repo_name)

    def get_filtered_branches(self) -> List[str]:
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

    def get_last_commit_id(self) -> str:
        """
        Returns commit id of last commit
        """
        return str(self.__repository.rev_parse("HEAD"))

    def cherrypick_commit_across_all_branches(self, commit_id) -> None:
        """
        Cherrypick git repository
        """
        branches = self.get_filtered_branches()

        # Cherrypick each branch
        for i, branch in enumerate(branches):

            # Attempt to checkout to branch
            try:
                self.checkout_to_branch(branch)

            # If checkout failed
            except CheckoutFailedError as err:
                print("Exception occurred while checking out to branch")
                print(err)
                user_input.prompt_user_to_exit_or_continue()

            # Successful checkout to branch
            else:
                # Attempt to cherrypick branch
                try:
                    self.__cherrypick_branch(commit_id)

                # Check if merge conflict occurred
                except MergeConflictError:
                    output.warn_user_of_merge_conflict(branch)

                    self.open_repository_in_vscode()

                    user_input.prompt_user_to_resolve_merge_conflict()

                    # Attempt to add changes and continue cherrypick
                    try:
                        self.add_changes_to_branch()
                        self.__continue_cherrypicking_branch()

                    # Create empty commit if error occurs
                    # TODO: figure out what exception is being thrown here
                    except Exception as err:
                        print(
                            "Exception occurred while adding and continuing cherrypick"
                        )
                        print(err)
                        print(type(err))
                        self.__commit_changes_allow_empty()

            # Inform user of successful cherry-pick, branch complete
            print(
                f"[{colors.OKCYAN}{(i + 1) * 100 / len(branches):.1f}%{colors.ENDC}]{colors.ENDC} {branch}: {colors.OKGREEN}[COMPLETE]{colors.ENDC}"
            )

    def open_repository_in_vscode(self):
        """Opens repository code in VS Code"""
        subprocess.check_output(f"code {self.get_repository_dir()}", shell=True)

    def get_minified_secure_branch(self) -> List[str]:
        """
        Gets the secure branch of a minified app. Minified app's secure branch starts with 'secure'
        """
        secure_branches = []

        for branch in self.get_filtered_branches():

            # Check if branch starts with 'secure'
            if jira.FULL_APP_SECURE_BRANCH in branch:
                secure_branches.append(branch)

        return secure_branches

    def __clone_repository(self) -> Repo:
        """
        Clone repository and return valid instance. Handle errors for invalid repository
        """
        git_url = f"{jira.SCW_GIT_URL}/{self.__repo_name}.git"
        repository_dir = self.get_repository_dir()

        # If repo folder already exists, remove it
        if os.path.isdir(repository_dir):

            # Delete repository
            subprocess.check_output(f"sudo rm -r {repository_dir}", shell=True)

        # Clone repository
        Repo.clone_from(git_url, repository_dir)

        # Create repository object
        repo = Repo(repository_dir)

        return repo
