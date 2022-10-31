"""
Manual bug fixing script that prints manual instructions to the console to lead the user through
fixing a bug in the Git repository, committing, cherrypicking, and manually transitioning Jira
issues
"""


import sys
import webbrowser
from git import GitError
from bugfixpy.constants import colors, headers, instructions, jira
from bugfixpy.git.repository import Repository
from bugfixpy.utils import user_input
from bugfixpy.formatter import Text, text
from bugfixpy.scripts.git import fix_branches_in_repository


# Main function runs bug-fix program
def run(test_mode: bool) -> None:
    """
    Main bug fixing function. Checks the mode, scrapes the CMS, opens the repository,
    and walks the user through the steps to fix the bug in all branches necessary.
    """
    if test_mode:
        Text(headers.TEST_MODE, colors.HEADER).display()

    # Get name of the git repository
    repo_name = user_input.get_repository_name()

    # Attempt to create repository
    try:
        repository = Repository(repo_name)
    except GitError:
        print(f"{colors.FAIL}Git Error: configure SSH key first{colors.ENDC}")
        sys.exit(1)

    # Print Details about the repository
    Text("Repo:", repo_name, colors.OKCYAN).display()
    Text("Branches:", repository.get_num_branches(), colors.OKCYAN).display()

    # Print whether the repository is a full app or minified app
    if repository.is_full_app():
        Text("Type:", "Full App", colors.OKCYAN).display()
    else:
        Text("Type:", "Minified App", colors.OKCYAN).display()

    # Run bug fix on repository
    fix_branches_in_repository(repository)

    # If test mode, don't push to repository
    if test_mode:
        print(instructions.PROMPT_FOR_ENTER_PUSH_DISABLED)
    else:
        print(instructions.PROMPT_FOR_ENTER_PUSH_ENABLED)

        # Push commit to the repository
        repository.push_fix_to_github()

    # Collect results from repository after running bug fix
    fix_messages = repository.get_fix_messages()
    repo_was_cherrypicked = repository.did_cherrypick_run()
    is_chunk_fixing_required = repository.did_number_of_lines_change()

    print(instructions.STEP_ONE_CLOSE_CHLRQ)

    # Print out fix messages
    print(text.format_fix_messages(fix_messages))

    print(instructions.STEP_TWO_LINK_CHLRQ)

    if repo_was_cherrypicked:

        chlc = user_input.get_chlc()

        # Open web browser to bulk transition tickets linked to the application CHLC
        webbrowser.open(jira.BULK_TRANSITION_JQL_URL.format(chlc=chlc))

        print(instructions.CHERRY_PICKING_MANUAL_STEPS)
    else:
        print(instructions.NO_CHERRY_PICKING_MANUAL_STEPS)

    # Notify user to check chunks if lines were added
    if is_chunk_fixing_required:
        print(instructions.UPDATE_CMS_AND_FIX_CHUNKS_REMINDER)
    else:
        print(instructions.UPDATE_CMS_REMINDER)

    print(instructions.BUG_FIX_COMPLETE)
