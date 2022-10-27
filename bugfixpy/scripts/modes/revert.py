"""Mode to revert previous commits in repository"""

import sys
from git import GitError
from bugfixpy.utils import user_input
from bugfixpy.git.gitrepository import GitRepository
from bugfixpy.constants import colors, headers, instructions
from bugfixpy.formatter import Text
from bugfixpy.scripts.git import revert_commit_in_repository


def run(test_mode):
    """
    Revert a commit in the git repository
    """
    commit_id = None
    Text("Revert mode enabled", colors.HEADER).display()

    if test_mode:
        Text(headers.TEST_MODE, colors.HEADER).display()

    # Get name of the git repository
    repo_name = user_input.get_repository_name()

    # Attempt to create repository
    try:
        repository = GitRepository(repo_name)
    except GitError:
        # Check for invalid repo name
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

    while not commit_id:
        commit_id = input("Enter commit ID: ")
        if not repository.branch_contains_commit_id(commit_id):
            commit_id = None

    # Run bug fix on repository
    revert_commit_in_repository(repository, commit_id)

    # If test mode, don't push to repository
    if test_mode:
        input(instructions.PROMPT_FOR_ENTER_PUSH_DISABLED)
    else:
        input(instructions.PROMPT_FOR_ENTER_PUSH_ENABLED)

        # Push commit to the repository
        repository.push_fix_to_github()

    print("Revert Complete.")
