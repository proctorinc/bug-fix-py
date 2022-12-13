"""
Instruction constants to direct users through bug fix process
"""


from . import colors

PROMPT_FOR_ENTER_PUSH_ENABLED = f"""\n{colors.HEADER}Press {colors.OKGREEN}[Enter]{colors.HEADER} to push to repo{colors.ENDC}"""

PROMPT_FOR_ENTER_PUSH_DISABLED = (
    f"""\n\n{colors.HEADER}Push Disabled. Press [ENTER] to continue{colors.ENDC}"""
)

CHERRY_PICKING_MANUAL_STEPS = f"""{colors.WARNING}
Follow these steps in the open tab
1. Bulk change all -> Select all -> Transition -> FEEDBACK OPEN -> confirm
2. Bulk change all -> Select all -> Transition -> FEEDBACK REVIEW -> confirm
3. Bulk change all -> Select all -> Edit -> Change assignee to 'Thomas Pieters' -> add CHLRQ-#### in comment [ex: CHLRQ-1234] -> confirm
{colors.ENDC}"""

NO_CHERRY_PICKING_MANUAL_STEPS = f"""{colors.WARNING}
Transition the challenge CHLC
1. Transition to FEEDBACK OPEN
2. Transition to FEEDBACK REVIEW
3. Set assignee to 'Thomas Pieters'
4. In comment, add link to CHLRQ
{colors.ENDC}"""

STEP_ONE_CLOSE_CHLRQ = f"""{colors.WARNING}
1. Close CHLRQ (add the commit in as a comment)
{colors.WHITE}"""

STEP_TWO_LINK_CHLRQ = f"""{colors.WARNING}
2. Link CHLRQ to challenge CHLC (choose 'relates to')
{colors.ENDC}"""

UPDATE_CMS_REMINDER = f"""{colors.HEADER}
COMPLETE THE FOLLOWING TASKS:
####################################
# 1. Update CMS branches to latest #
####################################
{colors.ENDC}"""

UPDATE_CMS_AND_FIX_CHUNKS_REMINDER = f"""{colors.HEADER}
COMPLETE THE FOLLOWING TASKS:
####################################
# 1. Update CMS branches to latest #
#                                  #
# 2. Commit added or removed lines #
#    Make sure chunks are correct  #
####################################
{colors.ENDC}"""

BUG_FIX_COMPLETE = f"""{colors.OKGREEN}{colors.BOLD}{colors.UNDERLINE}
Bug Fix Complete.{colors.ENDC}"""


PROMPT_USER_TO_MAKE_FIX = f"""\n{colors.UNDERLINE}{colors.OKGREEN}{colors.BOLD}Make the fix in VS Code{colors.ENDC}"""

PROMPT_USER_THAT_NO_FIX_WAS_MADE = f"""{colors.ENDC}{colors.FAIL}
No Changes detected in repository.
Press {colors.UNDERLINE}ctrl+s{colors.ENDC}{colors.FAIL} to save changes{colors.ENDC}"""

WARN_USER_OF_MERGE_CONFLICT = (
    "{colors.WARNING}[ !!! ]{colors.ENDC} {branch}: {colors.WARNING}MERGE CONFLICT"
)
