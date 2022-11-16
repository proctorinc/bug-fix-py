import sys

from bugfixpy.formatter import Text
from bugfixpy.constants import colors, headers, instructions
from bugfixpy.utils import validate


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
