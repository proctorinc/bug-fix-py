import sys
from git import GitError

from bugfixpy.git import Repository, FixBranches
from bugfixpy.jira import browser
from bugfixpy.utils import prompt_user, Text, formatter
from bugfixpy.utils.text import colors, headers, instructions


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

        FixBranches(repository, challenge_request_issue).run_fix()

        if test_mode:
            print(instructions.PROMPT_FOR_ENTER_PUSH_DISABLED)
        else:
            print(instructions.PROMPT_FOR_ENTER_PUSH_ENABLED)
            repository.push_all_branches()

        fix_messages = repository.get_fix_messages()
        repo_was_cherrypicked = repository.did_cherrypick_run()
        is_chunk_fixing_required = repository.did_number_of_lines_change()

        print(instructions.STEP_ONE_CLOSE_CHLRQ)
        print(formatter.format_fix_messages(fix_messages))
        print(instructions.STEP_TWO_LINK_CHLRQ)

        if repo_was_cherrypicked:

            application_creation_issue = prompt_user.get_application_creation_issue()

            browser.open_issue_in_browser(application_creation_issue)

            print(instructions.CHERRY_PICKING_MANUAL_STEPS)
        else:
            print(instructions.NO_CHERRY_PICKING_MANUAL_STEPS)

        if is_chunk_fixing_required:
            print(instructions.UPDATE_CMS_AND_FIX_CHUNKS_REMINDER)
        else:
            print(instructions.UPDATE_CMS_REMINDER)

        print(instructions.BUG_FIX_COMPLETE)
