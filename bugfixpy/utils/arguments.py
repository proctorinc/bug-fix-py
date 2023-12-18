import argparse
from argparse import ArgumentParser


def setup_parser() -> ArgumentParser:
    parser = argparse.ArgumentParser(
        description="bugfixpy automates the SCW bug fixing process"
    )

    parser.add_argument(
        "--setup",
        action="store_true",
        help="Run in setup mode. Setup all credentials for Jira API and CMS automation",
    )

    parser.add_argument(
        "--transition",
        action="store_true",
        help="Run in transition only mode for transitioning tickets in Jira without making changes",
    )

    parser.add_argument(
        "--revert",
        action="store_true",
        help="Run in revert mode to revert a previous git commit on an git repository",
    )

    parser.add_argument(
        "--auto",
        action="store_true",
        help="Run in auto mode. Enables Jira API for transitioning tickets"
        "and CMS webscraping for grabbing data",
    )

    parser.add_argument(
        "--manual",
        action="store_true",
        help="Enter repo name to run in repo mode. Opens repo in VS Code",
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Enable testing mode. Disabled pushing to git repository",
    )

    parser.add_argument(
        "--alert",
        action="store_true",
        help="Enable alert fixing mode",
    )

    return parser
