"""Quick way to check an application's code in VS Code without running fix mode"""

# Enter app name with autofill from what is in repo's already
# Or could we get a list of the repos in the github?

import sys
from git import GitError
from bugfixpy.utils import user_input
from bugfixpy.formatter import Text
from bugfixpy.git.gitrepository import GitRepository
from bugfixpy.constants import colors


def run() -> None:
    """
    Opens repository in VS Code and allows user to run other modes from this repo
    """

    # Allow a user to enter either a challenge id or an application name to open repo

    # Get name of the git repository
    repo_name = user_input.get_repository_name()

    # Attempt to create repository
    try:
        repository = GitRepository(repo_name)
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

    repository.open_code_in_editor()

    print("Running other modes is not supported yet.")
    print("Program finished.")
