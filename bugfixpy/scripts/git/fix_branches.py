from git import GitCommandError

from bugfixpy.git import Repository, FixResult, CherryPick
from bugfixpy.constants import jira, colors, instructions
from bugfixpy.jira import ChallengeRequestIssue
from bugfixpy.utils import prompt_user


def make_changes_in_repository(
    repository: Repository, challenge_request_issue: ChallengeRequestIssue
) -> FixResult:
    fix_messages = []
    repo_was_cherrypicked = False

    current_branch = prompt_user.for_branch_in_repository(repository)

    while current_branch != "":

        try:
            fix_message = __make_fix_and_commit(
                current_branch, repository, challenge_request_issue
            )

            fix_messages.append(fix_message)

            if (
                repository.is_full_app()
                and current_branch == jira.FULL_APP_SECURE_BRANCH
            ):

                commit_id = repository.get_last_commit_id()

                print("\nCherry-picking Branches...")
                CherryPick(repository, commit_id).across_all_branches()

                repo_was_cherrypicked = True

        except KeyboardInterrupt:
            print(
                f'\n{colors.FAIL}Fixing branch "{current_branch}" aborted.{colors.ENDC}'
            )

        current_branch = prompt_user.for_next_branch_or_to_continue(repository)

        print(colors.ENDC, end="")

    return FixResult(
        fix_messages=fix_messages,
        repo_was_cherrypicked=repo_was_cherrypicked,
        is_chunk_fixing_required=True,
    )


def __make_fix_and_commit(
    branch: str, repository: Repository, challenge_request_issue: ChallengeRequestIssue
) -> str:
    successful_commit = False

    repository.checkout_to_branch(branch)

    print(instructions.PROMPT_USER_TO_MAKE_FIX)

    repository.open_code_in_editor()

    fix_message = prompt_user.for_descripton_of_fix()

    while not successful_commit:
        try:
            repository.add_changes()

            repository.commit_changes_with_message(
                challenge_request_issue.get_issue_id() + ": " + fix_message
            )

        except GitCommandError as err:
            print(err)
            print(instructions.PROMPT_USER_THAT_NO_FIX_WAS_MADE)

            prompt_user.to_press_enter()

        else:
            successful_commit = True

    return fix_message
