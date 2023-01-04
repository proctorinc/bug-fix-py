import sys

from bugfixpy.git import Repository
from bugfixpy.utils import prompt_user
from bugfixpy.utils.text import colors, instructions
from bugfixpy.utils.text import Text


class RepositoryMode:
    __repository: Repository

    def get_repository(self) -> Repository:
        return self.__repository

    def clone_repository(self, repository_name: str) -> None:
        try:
            print("Cloning Repository...", end="")
            self.__repository = Repository(repository_name)

            self.print_repository_details()
        except ValueError:
            Text("Error getting repository", colors.FAIL).display()
            sys.exit(1)

    def clone_repository_from_user_input(self) -> None:
        repository_name = prompt_user.for_repository_name()
        self.clone_repository(repository_name)

    def print_repository_details(self) -> None:
        Text("[Done]", colors.OKGREEN).display()
        Text("Branches:", self.__repository.get_num_branches(), colors.OKCYAN).display()

        if self.__repository.is_full_app():
            Text("Type", "Full App", colors.OKCYAN).display()
        else:
            Text("Type:", "Minified App", colors.OKCYAN).display()

    def push_fix_to_github_if_not_in_test_mode(self, test_mode: bool) -> None:
        try:
            if test_mode:
                print(f"{colors.HEADER}Test mode enabled. Push skipped{colors.ENDC}")
            else:
                input(instructions.PROMPT_FOR_ENTER_PUSH_ENABLED)
                self.__repository.push_all_branches()
                print("Pushed successfully")
        except KeyboardInterrupt:
            print(f"\n{colors.FAIL}Skipped push to repository{colors.ENDC}")
