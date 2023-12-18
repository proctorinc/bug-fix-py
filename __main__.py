import sys

from bugfixpy.utils import validate
from bugfixpy.utils.text import colors
from bugfixpy.utils.arguments import setup_parser
from bugfixpy.modes import (
    TransitionMode,
    AutomaticMode,
    ManualMode,
    ViewRepository,
    RevertCommit,
    SetupCredentials,
    AlertMode,
)


def main() -> None:
    parser = setup_parser()
    args = parser.parse_args()

    if len(sys.argv) > 2 and not (
        args.test and (args.auto or args.revert or args.manual or args.alert)
    ):
        parser.error("Multiple flags cannot be enabled at the same time")

    if args.setup:
        SetupCredentials().start()
    elif args.transition:
        TransitionMode().start()
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
    elif args.alert:
        AlertMode(args.test).start()
    else:
        ViewRepository().start()


try:
    main()

except KeyboardInterrupt:
    print(f"\n{colors.FAIL}Exited program.")
    sys.exit(0)
