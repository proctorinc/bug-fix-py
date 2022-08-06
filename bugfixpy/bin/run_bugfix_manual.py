import webbrowser

from git import GitError

from bugfixpy import utils
from bugfixpy.constants import colors, headers, instructions
from bugfixpy.git import GitRepository
from bugfixpy.utils import Text


# Main function runs bug-fix program
def main(test_mode: bool):
    """
    Main bug fixing function. Checks the mode, scrapes the CMS, opens the repository,
    and walks the user through the steps to fix the bug in all branches necessary.
    """
    if test_mode:
        print(Text(headers.TEST_MODE, colors.HEADER))

    # TODO: add this to utils.input
    repo_name = input("Enter repo name: ")

    # Attempt to create repository
    try:
        repository = GitRepository(repo_name)
    except GitError as err:
        print(err)
        exit(1)

    # Print Details about the repository
    print(Text("Repo:", repo_name, colors.OKCYAN))
    print(Text("Branches:", repository.get_num_branches(), colors.OKCYAN))

    # Print whether the repository is a full app or minified app
    if repository.is_full_app():
        print(Text("Type:", "Full App", colors.OKCYAN))
    else:
        print(Text("Type:", "Minified App", colors.OKCYAN))

    # Run bug fix on repository
    repository.run_bug_fix()

    # If test mode, don't push to repository
    if test_mode:
        input(instructions.PROMPT_FOR_ENTER_PUSH_DISABLED)
    else:
        input(instructions.PROMPT_FOR_ENTER_PUSH_ENABLED)

        # Push commit to the repository
        repository.push()

    # Collect results from repository after running bug fix
    fix_messages = repository.get_fix_messages()
    repo_was_cherrypicked = repository.did_cherrypick_run()
    is_chunk_fixing_required = repository.did_number_of_lines_change()

    print(instructions.STEP_ONE_CLOSE_CHLRQ)

    # Print out fix messages
    utils.print_fix_messages(fix_messages)

    print(instructions.STEP_TWO_LINK_CHLRQ)

    if repo_was_cherrypicked:
        chlc = utils.get_chlc()
        # input('Enter application CHLC number [Ex: 1234]: ')

        # Open web browser to bulk transition tickets linked to the application CHLC
        webbrowser.open(
            f"https://securecodewarrior.atlassian.net/browse/CHLC-{chlc}?jql=project%20%3D%20%27CHLC%27%20and%20issuetype%3D%20challenge%20and%20issue%20in%20linkedIssues(%27CHLC-{chlc}%27)%20ORDER%20BY%20created%20DESC"
        )

        print(instructions.CHERRY_PICKING_MANUAL_STEPS)
    else:
        print(instructions.NO_CHERRY_PICKING_MANUAL_STEPS)

    # Notify user to check chunks if lines were added
    if is_chunk_fixing_required:
        print(instructions.UPDATE_CMS_AND_FIX_CHUNKS_REMINDER)
    else:
        print(instructions.UPDATE_CMS_REMINDER)

    print(instructions.BUG_FIX_COMPLETE)
