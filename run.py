#!/usr/bin/env python3

import sys
import argparse
from src import (
    bugfix,
    setup_credentials,
    transition,
    revert
)

def main():
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='bug-fix-py automates the SCW bug fixing process')

    # Setup switch
    parser.add_argument('--setup', action='store_true',
        help='Run in setup mode. Setup all credentials for Jira API and CMS automation')

    # Jira transition mode switch
    parser.add_argument('--transition', action='store_true',
        help='Run in transition only mode for transitioning tickets in Jira without making changes')

    # Commit revert mode switch
    parser.add_argument('--revert', action='store_true',
        help='Run in revert mode to revert a previous git commit on an git repository')

    # Auto transitioning on switch
    parser.add_argument('--auto', action='store_true',
        help='Run in auto mode. Enables Jira API for transitioning tickets and CMS webscraping for grabbing data')

    # No push switch
    parser.add_argument('--test', action='store_true',
        help='Enable testing mode. Disabled pushing to git repository')

    # Required repository positional argument
    parser.add_argument('--repo', type=str, help='Enter repo name to run in repo mode. Opens repo in VS Code')

    # Auto transitioning on switch
    # parser.add_argument('--debug', action='store_true',
    #     help='Enable debug mode (In development)')

    # Parse arguments
    args = parser.parse_args()

    if len(sys.argv) > 2 and not (args.test and args.auto):
        parser.error('Multiple flags cannot be enabled at the same time')

    if args.setup:
        setup_credentials.run()
    elif args.transition:
        transition.run()
    elif args.revert:
        revert.run()
    else:
        bugfix.run(args.auto, args.test)

if __name__ == '__main__':
    main()