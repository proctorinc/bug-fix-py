#!/usr/bin/env python3
import sys
import argparse
import os
from src import bin, utils
from src.constants import colors
from src.utils import Text, validate


def main():
    # Instantiate the parser
    parser = argparse.ArgumentParser(
        description="bug-fix-py automates the SCW bug fixing process"
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
        help="Run in auto mode. Enables Jira API for transitioning tickets and CMS webscraping for grabbing data",
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

    # Challenge ID positional argument
    parser.add_argument(
        "--cid", type=str, help="Enter challenge id of challenge to bug fix"
    )

    # Auto transitioning on switch
    # parser.add_argument('--debug', action='store_true',
    #     help='Enable debug mode (In development)')

    # Parse arguments
    args = parser.parse_args()

    if len(sys.argv) > 2 and not (args.test and args.auto):
        parser.error("Multiple flags cannot be enabled at the same time")

    #
    #
    # More validation checks for arguments
    #
    #

    # Run program mode based off of flags input
    if args.setup:
        bin.run_setup.main()
    elif args.transition:
        bin.run_transition.main()
    elif args.revert:
        bin.run_revert.main()
    elif args.auto:
        if not args.test and not validate.has_credentials():
            utils.print_missing_credentials()
        bin.run_bugfix.main(args.test)
    else:
        if not args.test and not validate.has_credentials():
            utils.print_missing_credentials()
        bin.run_bugfix_manual.main(args.test)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        Text("\nExited program.", colors.FAIL).display()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
