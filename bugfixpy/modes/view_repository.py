from bugfixpy.utils import prompt_user, validate
from bugfixpy.utils.text import colors, instructions

from .types import RunnableMode, RepositoryMode, ScraperMode


class ViewRepository(RunnableMode, RepositoryMode, ScraperMode):

    MODE = "VIEW"

    def __init__(self) -> None:
        super().__init__(self.MODE, False)

    def run(self) -> None:
        self.clone_repository_from_challenge_id_or_repository_name()
        self.clone_repository_from_scraper_data()
        self.open_branch_from_repository_in_code_editor()

    def clone_repository_from_scraper_data(self) -> None:
        repository_name = self.get_scraper_data().application.repository_name
        self.clone_repository(repository_name)

    def open_branch_from_repository_in_code_editor(self) -> None:
        repository = self.get_repository()
        branch = prompt_user.for_branch_in_repository(repository)
        repository.checkout_to_branch(branch)
        repository.open_code_in_editor()

    def clone_repository_from_challenge_id_or_repository_name(self) -> None:
        name_or_id = input(f"Enter repository name or challenge id: {colors.WHITE}")
        print(colors.ENDC, end="")

        if validate.is_valid_challenge_id(name_or_id):
            print("Challenge ID entered")
            self.challenge_id = name_or_id
            self.scrape_cms_and_print_results()
        else:
            print("Repository name entered")
            self.clone_repository(name_or_id)

    def display_results(self) -> None:
        print(f"Repository opening in editor... {instructions.DONE}")
