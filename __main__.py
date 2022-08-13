"""
Main entry point for bugfixpy
"""


import sys
import argparse

from bugfixpy.scripts import modes
from bugfixpy.constants import colors
from bugfixpy.utils import validate, output
from bugfixpy.formatter import Text


def main() -> None:
    """
    Main method takes in arguments to decide which mode to run
    """
    # Instantiate the parser
    parser = argparse.ArgumentParser(
        description="bugfixpy automates the SCW bug fixing process"
    )

    # Setup switch
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Run in setup mode. Setup all credentials for Jira API and CMS automation",
    )

    # Jira transition mode switch
    parser.add_argument(
        "--transition",
        action="store_true",
        help="Run in transition only mode for transitioning tickets in Jira without making changes",
    )

    # Commit revert mode switch
    parser.add_argument(
        "--revert",
        action="store_true",
        help="Run in revert mode to revert a previous git commit on an git repository",
    )

    # Auto transitioning on switch
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Run in auto mode. Enables Jira API for transitioning tickets"
        "and CMS webscraping for grabbing data",
    )

    # No push switch
    parser.add_argument(
        "--test",
        action="store_true",
        help="Enable testing mode. Disabled pushing to git repository",
    )

    # Repository positional argument
    parser.add_argument(
        "--repo",
        type=str,
        help="Enter repo name to run in repo mode. Opens repo in VS Code",
    )

    # Parse arguments
    args = parser.parse_args()

    if len(sys.argv) > 2 and not (args.test and args.auto):
        parser.error("Multiple flags cannot be enabled at the same time")

    # Run program mode based off of flags input
    if args.setup:
        modes.setup.run()
    elif args.transition:
        modes.transition.run()
    elif args.revert:
        modes.revert.run()
    elif not args.auto:
        modes.manual_fix.run(args.test)
    elif not args.test and not validate.has_credentials():
        output.print_missing_credentials()
    else:
        modes.auto_fix.run(args.test)


try:
    main()
except KeyboardInterrupt:
    Text("\nExited program.", colors.FAIL).display()
    sys.exit(0)
