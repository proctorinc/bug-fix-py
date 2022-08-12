from . import colors

PROMPT_FOR_ENTER_PUSH_ENABLED = f"""{colors.HEADER}
Press [ENTER] to push to repo
{colors.ENDC}"""

PROMPT_FOR_ENTER_PUSH_DISABLED = f"""{colors.HEADER}
Push Disabled. Press [ENTER] to continue
{colors.ENDC}"""

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
