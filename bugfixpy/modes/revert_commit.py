from bugfixpy.utils import validate
from bugfixpy.git import Repository
from bugfixpy.constants import colors, headers, instructions
from bugfixpy.formatter import Text
from bugfixpy.scripts.git import revert_commit_in_repository
from . import utils


class RevertCommit:

    test_mode: bool
    repository: Repository

    def __init__(self, test_mode) -> None:
        self.test_mode = test_mode

    @classmethod
    def run(cls, test_mode) -> None:
        revert_commit = cls(test_mode)

        revert_commit.display_revert_mode_headers()

        revert_commit.clone_repository_from_challenge_id_or_repository_name()

        revert_commit.get_commit_id_and_revert_commit()

        revert_commit.push_fix_to_github_if_not_in_test_mode()

        print("Revert Complete.")

    def get_commit_id_and_revert_commit(self) -> None:
        commit_id = None
        while not commit_id:
            commit_id = input("Enter commit ID: ")
            if not self.repository.branch_contains_commit_id(commit_id):
                commit_id = None

        revert_commit_in_repository(self.repository, commit_id)

    # TODO: duplicate in automatic_fix
    def push_fix_to_github_if_not_in_test_mode(self) -> None:
        try:
            if self.test_mode:
                print(f"{colors.HEADER}Test mode enabled. Push skipped{colors.ENDC}")
            else:
                input(instructions.PROMPT_FOR_ENTER_PUSH_ENABLED)
                self.repository.push_fix_to_github()
        except KeyboardInterrupt:
            print(f"\n{colors.FAIL}Skipped push to repository{colors.ENDC}")

    # TODO: duplicate in view_repository
    def clone_repository_from_challenge_id_or_repository_name(self) -> None:
        name_or_id = input(f"Enter repository name or challenge id: {colors.WHITE}")
        print(colors.ENDC, end="")

        if validate.is_valid_challenge_id(name_or_id):
            print("Challenge ID entered")
            challenge_data = utils.scrape_challenge_data_from_cms(name_or_id)
            repo_name = challenge_data.application.repository_name
        else:
            print("Repository name entered")
            repo_name = name_or_id

        self.repository = utils.clone_the_challenge_repository(repo_name)

    # TODO: semi duplicate in modes/utils.py
    def display_revert_mode_headers(self) -> None:
        Text("Revert mode enabled", colors.HEADER).display()

        if self.test_mode:
            Text(headers.TEST_MODE, colors.HEADER).display()
