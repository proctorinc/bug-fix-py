from bugfixpy.utils import prompt_user, validate
from bugfixpy.git import Repository
from bugfixpy.utils.text import colors
from . import utils


class ViewRepository:

    repository: Repository

    @classmethod
    def run(cls) -> None:
        view_repository = cls()

        view_repository.clone_repository_from_challenge_id_or_repository_name()

        view_repository.open_branch_from_repository_in_code_editor()

        print("Running other modes from this repo is not supported yet.")

    def open_branch_from_repository_in_code_editor(self) -> None:
        branch = prompt_user.for_branch_in_repository(self.repository)

        self.repository.checkout_to_branch(branch)

        self.repository.open_code_in_editor()

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
