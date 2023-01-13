import sys

from bugfixpy.git import Repository
from bugfixpy.utils import prompt_user
from bugfixpy.utils.text import colors, instructions


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
            print(f"{colors.FAIL}Error getting repository")
            sys.exit(1)

    def clone_repository_from_user_input(self) -> None:
        repository_name = prompt_user.for_repository_name()
        self.clone_repository(repository_name)

    def print_repository_details(self) -> None:
        num_branches = len(self.__repository.get_branches())
        print(instructions.DONE)
        print(f"Branches: {colors.OKCYAN}{num_branches}{colors.ENDC}")

        if self.__repository.is_full_app():
            print(f"Type {colors.OKCYAN}Full App{colors.ENDC}")
        else:
            print(f"Type: {colors.OKCYAN}Minified App{colors.ENDC}")

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
