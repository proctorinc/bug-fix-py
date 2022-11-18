from bugfixpy.utils import prompt_user, validate
from bugfixpy.git import Repository
from . import utils


def run() -> None:
    repository = clone_repository_from_challenge_id_or_repository_name()

    open_branch_from_repository_in_code_editor(repository)

    print("Running other modes from this repo is not supported yet.")


def open_branch_from_repository_in_code_editor(repository) -> None:
    branch = prompt_user.for_branch_in_repository(repository)

    repository.checkout_to_branch(branch)

    repository.open_code_in_editor()


def clone_repository_from_challenge_id_or_repository_name() -> Repository:
    name_or_id = input("Enter repository name or challenge id: ")

    if validate.is_valid_challenge_id(name_or_id):
        print(f"Looking for challenge ID: {name_or_id}")
        challenge_data = utils.scrape_challenge_data_from_cms(name_or_id)
        repo_name = challenge_data.application.repository_name
    else:
        print(f"Looking for repository: {name_or_id}")
        repo_name = name_or_id

    repository = utils.clone_the_challenge_repository(repo_name)

    return repository
