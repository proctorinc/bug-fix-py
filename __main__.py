import sys
import argparse

from bugfixpy.utils.text import colors
from bugfixpy.utils import validate
from bugfixpy.modes import (
    TransitionIssuesMode,
    AutomaticMode,
    ManualMode,
    ViewRepository,
    RevertCommit,
    SetupCredentials,
)


def main() -> None:
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

    args = parser.parse_args()

    if len(sys.argv) > 2 and not (
        args.test and (args.auto or args.revert or args.manual)
    ):
        parser.error("Multiple flags cannot be enabled at the same time")

    if args.setup:
        SetupCredentials.run()
    elif args.transition:
        TransitionIssuesMode().start()
    elif args.revert:
        RevertCommit.run(args.test)
    elif args.manual:
        ManualMode(args.test).start()
    elif not args.test and not validate.has_valid_credentials():
        print(
            f"{colors.FAIL}Credentials are not setup\nRun: python3 bugfixpy --setup{colors.ENDC}"
        )
    elif args.auto:
        AutomaticMode(args.test).start()
    else:
        ViewRepository.run()


try:
    main()

except KeyboardInterrupt:
    print(f"\n{colors.FAIL}Exited program.")
    sys.exit(0)
