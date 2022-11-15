import sys

from bugfixpy.git.fix_result import FixResult
from bugfixpy.scraper import CmsScraper
from bugfixpy.constants import colors, headers, instructions
from bugfixpy.git.repository import Repository
from bugfixpy.scraper.scraper_data import ScraperData
from bugfixpy.scripts import transition
from bugfixpy.scripts.git import make_changes_in_repository
from bugfixpy.formatter import Text
from bugfixpy.utils import user_input, validate
from bugfixpy.exceptions import RequestFailedError
from bugfixpy.jira.issue import (
    ChallengeRequestIssue,
)


def run(test_mode: bool) -> None:
    print_mode_headers(test_mode)
    challenge_data = scrape_challenge_data_from_cms()
    repository = clone_the_challenge_repository(
        challenge_data.application.repository_name
    )
    challenge_request_issue = user_input.get_challenge_request_issue()
    fix_results = make_changes_in_repository(repository, challenge_request_issue)
    push_fix_to_github_if_not_in_test_mode(repository, test_mode)
    transition_challenge_issues_with_results(
        fix_results, challenge_data, challenge_request_issue
    )
    print_end_instructions_based_off_of_results(fix_results)


def print_mode_headers(test_mode) -> None:
    Text(headers.AUTO_MODE_ENABLED, colors.HEADER).display()

    if test_mode:
        Text(headers.TEST_MODE, colors.HEADER).display()

    elif not validate.has_valid_credentials():
        Text(
            "Invalid API credentials. Run with --setup to change credentials",
            colors.FAIL,
        ).display()
        sys.exit(1)


def scrape_challenge_data_from_cms() -> ScraperData:
    try:
        challenge_id = user_input.get_challenge_id()
        print("Collecting data from CMS...", end="")
        scraper_data = CmsScraper.scrape_challenge_data(challenge_id)

        print_scraper_data(scraper_data)
    except RequestFailedError as err:
        Text(f"\n{err}", colors.FAIL).display()
        sys.exit(1)
    except Exception as err:
        Text("\nUnknown Error", err, colors.FAIL).display()
        sys.exit(1)

    return scraper_data


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


def print_repository_details(repository) -> None:
    Text("[Done]", colors.OKGREEN).display()
    Text("Branches:", repository.get_num_branches(), colors.OKCYAN).display()

    # TODO: get is full app from Scraper instead of repo
    if repository.is_full_app():
        Text("Type", "Full App", colors.OKCYAN).display()
    else:
        Text("Type:", "Minified App", colors.OKCYAN).display()


def push_fix_to_github_if_not_in_test_mode(repository, test_mode) -> None:
    try:
        if test_mode:
            print(f"{colors.HEADER}Test mode enabled. Push skipped{colors.ENDC}")
        else:
            input(instructions.PROMPT_FOR_ENTER_PUSH_ENABLED)
            repository.push_fix_to_github()
    except KeyboardInterrupt:
        print(f"\n{colors.FAIL}Skipped push to repository{colors.ENDC}")


def transition_challenge_issues_with_results(
    fix_result: FixResult,
    challenge_data: ScraperData,
    challenge_request_issue: ChallengeRequestIssue,
) -> None:
    try:
        transition.transition_jira_issues(
            fix_result,
            challenge_data,
            challenge_request_issue,
        )

    except Exception as err:
        print(err)
        sys.exit(1)


def print_end_instructions_based_off_of_results(changes_results) -> None:
    is_chunk_fixing_required = changes_results.is_chunk_fixing_required
    if is_chunk_fixing_required:
        print(instructions.UPDATE_CMS_AND_FIX_CHUNKS_REMINDER)
    else:
        print(instructions.UPDATE_CMS_REMINDER)

    print(instructions.BUG_FIX_COMPLETE)
