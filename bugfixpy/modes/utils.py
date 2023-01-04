import sys

from bugfixpy.utils import Text
from bugfixpy.git import Repository
from bugfixpy.utils import validate, prompt_user
from bugfixpy.utils.text import headers
from bugfixpy.cms import CmsScraper, ScraperData
from bugfixpy.exceptions import RequestFailedError
from bugfixpy.utils.text import colors, instructions


def scrape_challenge_data_from_cms(challenge_id=None) -> ScraperData:
    try:
        if not challenge_id:
            challenge_id = prompt_user.for_challenge_id()
        print("Collecting data from CMS...", end="")
        scraper_data = CmsScraper.scrape_challenge_data(challenge_id)

        print_scraper_data(scraper_data)
    except RequestFailedError as err:
        Text(f"\n{err}", colors.FAIL).display()
        sys.exit(1)
    except Exception as err:
        Text("[Failed]\nInvalid challenge ID entered", colors.FAIL).display()
        sys.exit(1)

    return scraper_data


def print_mode_headers(test_mode=False) -> None:
    Text(headers.AUTO_MODE_ENABLED, colors.HEADER).display()

    if test_mode:
        Text(headers.TEST_MODE, colors.HEADER).display()

    elif not validate.has_valid_credentials():
        Text(
            "Invalid API credentials. Run with --setup to change credentials",
            colors.FAIL,
        ).display()
        sys.exit(1)


def print_repository_details(repository) -> None:
    Text("[Done]", colors.OKGREEN).display()
    Text("Branches:", repository.get_num_branches(), colors.OKCYAN).display()

    # TODO: get is full app from Scraper instead of repo
    if repository.is_full_app():
        Text("Type", "Full App", colors.OKCYAN).display()
    else:
        Text("Type:", "Minified App", colors.OKCYAN).display()


def print_end_instructions_based_off_of_results(changes_results) -> None:
    is_chunk_fixing_required = changes_results.is_chunk_fixing_required
    if is_chunk_fixing_required:
        print(instructions.UPDATE_CMS_AND_FIX_CHUNKS_REMINDER)
    else:
        print(instructions.UPDATE_CMS_REMINDER)

    print(instructions.BUG_FIX_COMPLETE)


def print_scraper_data(scraper_data) -> None:
    Text("[Done]", colors.OKGREEN).display()
    Text(
        "Challenge CHLC:", scraper_data.challenge.chlc.get_issue_id(), colors.OKCYAN
    ).display()
    Text(
        "Application CHLC:", scraper_data.application.chlc.get_issue_id(), colors.OKCYAN
    ).display()
    Text("Repo:", scraper_data.application.repository_name, colors.OKCYAN).display()


def clone_the_challenge_repository(repository_name) -> Repository:
    try:
        print("Cloning Repository...", end="")
        repository = Repository(repository_name)

        print_repository_details(repository)
    except ValueError:
        Text("Error getting repository", colors.FAIL).display()
        sys.exit(1)

    return repository


def push_fix_to_github_if_not_in_test_mode(
    test_mode: bool, repository: Repository
) -> None:
    try:
        if test_mode:
            print(f"{colors.HEADER}Test mode enabled. Push skipped{colors.ENDC}")
        else:
            input(instructions.PROMPT_FOR_ENTER_PUSH_ENABLED)
            repository.push_all_branches()
            print("Pushed successfully")
    except KeyboardInterrupt:
        print(f"\n{colors.FAIL}Skipped push to repository{colors.ENDC}")
