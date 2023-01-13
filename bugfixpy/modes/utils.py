import sys

from bugfixpy.utils import validate
from bugfixpy.utils.text import headers
from bugfixpy.utils.text import colors, instructions


def print_mode_headers(test_mode=False) -> None:
    print(colors.HEADER, headers.AUTO_MODE_ENABLED, colors.ENDC, sep="")

    if test_mode:
        print(headers.TEST_MODE, colors.HEADER, colors.ENDC, sep="")

    elif not validate.has_valid_credentials():
        print(
            colors.FAIL,
            "Invalid API credentials. Run with --setup to change credentials",
            colors.ENDC,
            sep="",
        )
        sys.exit(1)


def print_repository_details(repository) -> None:
    print(instructions.DONE)
    print(
        "Branches:",
        colors.OKCYAN,
        repository.get_num_branches(),
        colors.ENDC,
        sep="",
    )

    if repository.is_full_app():
        print(
            "Type",
            colors.OKCYAN,
            "Full App",
            colors.ENDC,
            sep="",
        )
    else:
        print(
            "Type:",
            colors.OKCYAN,
            "Minified App",
            colors.ENDC,
            sep="",
        )


def print_end_instructions_based_off_of_results(is_chunk_fixing_required) -> None:
    if is_chunk_fixing_required:
        print(instructions.UPDATE_CMS_AND_FIX_CHUNKS_REMINDER)
    else:
        print(instructions.UPDATE_CMS_REMINDER)

    print(instructions.BUG_FIX_COMPLETE)
