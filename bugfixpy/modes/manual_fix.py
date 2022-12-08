import sys
import webbrowser
from git import GitError

from bugfixpy.constants import colors, headers, instructions, jira
from bugfixpy.git import Repository
from bugfixpy.utils import prompt_user
from bugfixpy.formatter import Text, text
from bugfixpy.scripts.git import make_changes_in_repository


class ManualFix:
    @classmethod
    def run(cls, test_mode: bool) -> None:
        if test_mode:
            Text(headers.TEST_MODE, colors.HEADER).display()

        repo_name = prompt_user.for_repository_name()

        try:
            repository = Repository(repo_name)
        except GitError:
            print(f"{colors.FAIL}Git Error: configure SSH key first{colors.ENDC}")
            sys.exit(1)

        Text("Repo:", repo_name, colors.OKCYAN).display()
        Text("Branches:", repository.get_num_branches(), colors.OKCYAN).display()

        if repository.is_full_app():
            Text("Type:", "Full App", colors.OKCYAN).display()
        else:
            Text("Type:", "Minified App", colors.OKCYAN).display()

        challenge_request_issue = prompt_user.get_challenge_request_issue()

        make_changes_in_repository(repository, challenge_request_issue)

        if test_mode:
            print(instructions.PROMPT_FOR_ENTER_PUSH_DISABLED)
        else:
            print(instructions.PROMPT_FOR_ENTER_PUSH_ENABLED)
            repository.push_fix_to_github()

        fix_messages = repository.get_fix_messages()
        repo_was_cherrypicked = repository.did_cherrypick_run()
        is_chunk_fixing_required = repository.did_number_of_lines_change()

        print(instructions.STEP_ONE_CLOSE_CHLRQ)
        print(text.format_fix_messages(fix_messages))
        print(instructions.STEP_TWO_LINK_CHLRQ)

        if repo_was_cherrypicked:

            application_creation_issue = prompt_user.get_application_creation_issue()

            webbrowser.open(
                jira.BULK_TRANSITION_JQL_URL.format(
                    chlc=application_creation_issue.get_issue_id()
                )
            )

            print(instructions.CHERRY_PICKING_MANUAL_STEPS)
        else:
            print(instructions.NO_CHERRY_PICKING_MANUAL_STEPS)

        if is_chunk_fixing_required:
            print(instructions.UPDATE_CMS_AND_FIX_CHUNKS_REMINDER)
        else:
            print(instructions.UPDATE_CMS_REMINDER)

        print(instructions.BUG_FIX_COMPLETE)
