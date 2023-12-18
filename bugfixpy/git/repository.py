import os
from typing import List
import subprocess
import shutil

from git import GitCommandError, GitError
from git.repo import Repo
from bugfixpy import git
from bugfixpy.exceptions import (
    MergeConflictError,
    CheckoutFailedError,
    ContinueCherryPickingFailedError,
)
from . import constants


class Repository:
    name: str
    repository: Repo
    branches: list[str]
    fix_messages: List[str]
    has_cherrypicked: bool

    def __init__(self, name: str) -> None:
        self.name = name
        self.fix_messages = []
        self.has_cherrypicked = False
        self.__delete_local_and_clone_repository()
        self.branches = self.__get_filtered_branches()

    def get_branches(self) -> list[str]:
        return self.branches

    def get_current_branch(self) -> str:
        return self.repository.active_branch.name

    def __delete_local_and_clone_repository(self) -> None:
        self.__delete_repository_if_exists()
        self.repository = self.clone_repository()

    def __delete_repository_if_exists(self) -> None:
        try:
            path = self.get_repository_dir()
            shutil.rmtree(path)
        except OSError:
            pass

    def get_num_branches(self) -> int:
        return len(self.branches)

    def is_full_app(self) -> bool:
        branches = self.branches

        return git.constants.FULL_APP_SECURE_BRANCH in branches

    def get_fix_messages(self) -> List[str]:
        return self.fix_messages

    def was_cherry_picked(self) -> bool:
        return self.has_cherrypicked

    def set_was_cherrypicked(self) -> None:
        self.has_cherrypicked = True

    def did_number_of_lines_change(self) -> bool:
        commit = self.repository.head.commit
        previous_commit = commit.parents[0]

        diffs = previous_commit.diff(commit)

        modified_filenames = [diff.b_path for diff in diffs]

        for diff in diffs:
            if diff.a_blob is None or diff.b_blob is None:
                if diff.a_blob is None:
                    modified_filenames.append((diff.b_path, "+"))
                else:
                    modified_filenames.append((diff.b_path, "-"))

        return len(modified_filenames) > 0

    def get_list_of_files_changed_in_commit(self, commit) -> list[str]:
        previous_commit = commit.parents[0]

        diffs = previous_commit.diff(commit)

        modified_filenames = [diff.b_path for diff in diffs]

        return modified_filenames

    def get_whether_commit_changed_length_of_file(self, commit) -> bool:
        return len(self.get_files_that_changed_length_due_to_commit(commit)) > 0

    def get_files_that_changed_length_due_to_commit(self, commit) -> list[str]:
        modified_files = []
        previous_commit = commit.parents[0]

        diffs = previous_commit.diff(commit)

        for diff in diffs:
            if diff.a_blob is not None and diff.b_blob is not None:
                if diff.a_blob.size != diff.b_blob.size:
                    modified_files.append(diff.b_path)

        return modified_files

    def push_all_branches(self) -> None:
        self.repository.git.push(all=True)

    def checkout_to_branch(self, branch: str) -> None:
        try:
            self.repository.git.checkout(branch)
        except GitCommandError as err:
            raise CheckoutFailedError(err) from err

    def add_changes(self) -> None:
        self.repository.git.add(u=True)

    def continue_cherrypicking(self) -> None:
        try:
            self.repository.git.cherry_pick("--continue")

        except GitCommandError as err:
            raise ContinueCherryPickingFailedError() from err
        except Exception as err:
            print(f"unhandled err: {err}")

    def commit_changes_with_message(self, message) -> None:
        self.repository.git.commit("-m", f'"{message}"')

    def commit_changes_allow_empty(self) -> None:
        self.repository.git.commit("--allow-empty", "-m", "Empty Commit")

    def cherry_pick(self, commit_id) -> None:
        try:
            self.repository.git.cherry_pick(commit_id)

        except GitCommandError as err:
            if "exit code(1)" in str(err):
                raise MergeConflictError() from err

    def get_repository_dir(self) -> str:
        return os.path.join(constants.REPO_DIR, self.name)

    def __is_not_excluded_branch(self, branch_name) -> bool:
        return branch_name not in constants.IGNORE_BRANCHES

    def __get_filtered_branches(self) -> List[str]:
        branch_names = [
            self.__parse_name_from_remote_branch(branch)
            for branch in self.repository.remote().refs
        ]
        filtered_branches = list(filter(self.__is_not_excluded_branch, branch_names))

        return filtered_branches

    def __parse_name_from_remote_branch(self, branch):
        return branch.name.split("origin/")[1]

    def get_last_commit_id(self) -> str:
        return str(self.repository.rev_parse("HEAD"))

    def branch_contains_commit_id(self, commit_id) -> bool:
        try:
            self.repository.git.branch("--contains", commit_id)

        except GitCommandError:
            return False

        return True

    def revert_commit(self, commit_id) -> None:
        result = subprocess.check_output(
            f"git -C {self.get_repository_dir()} revert {commit_id} &>/dev/null",
            shell=True,
        ).decode("utf-8")

        if not result:
            raise GitError("Error reverting commit")

        if "CONFLICT" in result:
            raise MergeConflictError("Merge conflict occurred")

    def has_merge_conflict(self) -> bool:
        print(
            "STATUS", self.repository.git.status(), "\n********************************"
        )
        return "Unmerged" in self.repository.git.status()

    def open_code_in_editor(self) -> None:
        subprocess.check_output(f"code {self.get_repository_dir()}", shell=True)

    def get_minified_secure_branch(self) -> List[str]:
        secure_branches = []

        for branch in self.branches:
            if constants.FULL_APP_SECURE_BRANCH in branch:
                secure_branches.append(branch)

        return secure_branches

    def clone_repository(self) -> Repo:
        git_url = f"{constants.SCW_GIT_URL}/{self.name}.git"
        repository_dir = self.get_repository_dir()

        return Repo.clone_from(git_url, repository_dir)

    def __str__(self) -> str:
        return self.name
