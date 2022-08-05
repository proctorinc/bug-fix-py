from . import colors

PROMPT_FOR_ENTER_PUSH_ENABLED = f"""
    {colors.HEADER}
    \nPress [ENTER] to push to repo
    {colors.ENDC}
    """

PROMPT_FOR_ENTER_PUSH_DISABLED = f"""
    {colors.HEADER}
    \nPush Disabled. Press [ENTER] to continue
    {colors.ENDC}
    """

CHERRY_PICKING_MANUAL_STEPS = f"""
    {colors.WARNING}
    \nFollow these steps in the open tab
    \n1. Bulk change all -> Select all -> Transition -> FEEDBACK OPEN -> confirm
    \n2. Bulk change all -> Select all -> Transition -> FEEDBACK REVIEW -> confirm
    \n3. Bulk change all -> Select all -> Edit -> Change assignee to 'Thomas Pieters' -> add CHLRQ-#### in comment [ex: CHLRQ-1234] -> confirm
    {colors.ENDC}'\
    """

NO_CHERRY_PICKING_MANUAL_STEPS = f"""
    {colors.WARNING}
    \nTransition the challenge CHLC
    \n1. Transition to FEEDBACK OPEN
    \n2. Transition to FEEDBACK REVIEW
    \n3. Set assignee to 'Thomas Pieters'
    \n4. In comment, add link to CHLRQ
    {colors.ENDC}
    """

STEP_ONE_CLOSE_CHLRQ = f"""
    {colors.WARNING}
    \n1. Close CHLRQ (add the commit in as a comment)
    {colors.WHITE}
    """

STEP_TWO_LINK_CHLRQ = f"""
    {colors.WARNING}
    2. Link CHLRQ to challenge CHLC (choose 'relates to')
    {colors.ENDC}
    """

UPDATE_CMS_REMINDER = f"""
    {colors.HEADER}
    \nCOMPLETE THE FOLLOWING TASKS:
    \n####################################
    \n# 1. Update CMS branches to latest #
    \n####################################
    {colors.ENDC}
    """

UPDATE_CMS_AND_FIX_CHUNKS_REMINDER = f"""
    {colors.HEADER}
    \nCOMPLETE THE FOLLOWING TASKS:
    \n####################################
    \n# 1. Update CMS branches to latest #
    \n#                                  #
    \n# 2. Commit added or removed lines #
    \n#    Make sure chunks are correct  #
    \n####################################
    {colors.ENDC}
    """

BUG_FIX_COMPLETE = f"""
    {colors.OKGREEN}
    {colors.BOLD}
    {colors.UNDERLINE}
    \nBug Fix Complete.
    {colors.ENDC}
    """
