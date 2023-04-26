from . import colors

PROMPT_FOR_ENTER_PUSH_ENABLED = f"""\n{colors.HEADER}Press {colors.OKGREEN}[Enter]{colors.HEADER} to push to repo{colors.ENDC}"""

PROMPT_FOR_ENTER_PUSH_DISABLED = (
    f"""\n\n{colors.HEADER}Push Disabled. Press [ENTER] to continue{colors.ENDC}"""
)

PROMPT_FOR_REPOSITORY_NAME = f"""{colors.WARNING}
 - Find the name of the repository from the application screen in the CMS
   Ex: If button shows {colors.UNDERLINE}SCWContent/opentasks{colors.ENDC}{colors.WARNING}, enter the name "{colors.UNDERLINE}opentasks{colors.ENDC}{colors.WARNING}"
{colors.ENDC}"""

PROMPT_FOR_CHALLENGE_REQUEST = f"""{colors.WARNING}
 - Find the Challenge Request Issue number in Jira
   Ex: If CHLRQ-1234 enter "{colors.UNDERLINE}CHLRQ-1234{colors.ENDC}{colors.WARNING}" or "{colors.UNDERLINE}1234{colors.ENDC}{colors.WARNING}"
{colors.ENDC}"""

TRANSITION_AND_CHECKOUT_STEPS = f"""{colors.WARNING}
Transition the Challenge Request Issue in Jira:
1. Transition CHLRQ to Planned (choose this month)
2. Transition CHLRQ to In Progress
3. Locate the branch to make the fix on (if secure, choose secure)
{colors.ENDC}"""

CHERRY_PICKING_MANUAL_STEPS = f"""{colors.WARNING}
Transition all Challenge Creation Issues in Jira
(tab will automatically open issues in Jira)
1. Bulk change all -> Select all -> Transition -> FEEDBACK OPEN -> confirm
2. Bulk change all -> Select all -> Transition -> FEEDBACK REVIEW -> confirm
3. Bulk change all -> Select all -> Edit -> Change assignee to Content Team Approver -> add CHLRQ-#### in comment [ex: CHLRQ-1234] -> confirm
{colors.ENDC}"""

NO_CHERRY_PICKING_MANUAL_STEPS = f"""{colors.WARNING}
Transition the Challenge Creation Issue in Jira
1. Transition to FEEDBACK OPEN
2. Transition to FEEDBACK REVIEW
3. Set assignee to Content Team Approver
4. In comment, add link to CHLRQ
{colors.ENDC}"""

CLOSE_CHALLENGE_REQUEST_STEPS = f"""{colors.WARNING}
Transition the Challenge Request Issue in Jira:
1. Close CHLRQ add a comment about the commit
2. Link CHLRQ to challenge CHLC (choose '{colors.UNDERLINE}relates to{colors.ENDC}{colors.WARNING}')
{colors.ENDC}"""

MERGE_CONFLICT_STEPS = f"""{colors.WARNING}
- Resolve all merge conflicts in repository in the code editor
  (editor will open automatically)
{colors.ENDC}"""

STEP_TWO_LINK_CHLRQ = f"""{colors.WARNING}
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
# 2. Fix all chunks in challenge   #
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

DONE = f"{colors.OKGREEN}[Done]{colors.ENDC}"
