import git
import os
import subprocess
from src import constants

def filter_branches(remote_refs):
    """
    Parse branches from remote refs and remove unwanted branches
    """
    filtered_branches = []

    # Loop over remote references
    for refs in remote_refs:

        # Remove origin/ from branch name
        branch = refs.name.split("origin/",1)[1]

        # Filter branches
        if branch not in JIRA_IGNORE_BRANCHES:
            filtered_branches.append(branch)

    return filtered_branches

def get_repository_dir(repo_name):
    """
    Returns absolute url for repository folder
    """
    return os.path.join(JIRA_REPO_DIR, repo_name)

def clone_repository(repo_name):
    """
    Clone repository and return valid instance. Handle errors for invalid repository
    """
    git_url = f'{JIRA_SCW_GIT_URL}/{repo_name}.git'
    repository_dir = get_repository_dir(repo_name)

    print(f'Cloning Repository...', end='')

    # If repo folder already exists, remove it
    if os.path.isdir(repository_dir):
        
        # Alert user of repo existing
        print(f'\nRepository cached. Resetting...', end='')

        # Delete repository
        subprocess.check_output(f'sudo rm -r {repository_dir}', shell=True)
    try:
        # Clone repository
        git.Repo.clone_from(git_url, repository_dir)
    
    except git.exc.GitError:
        print(f'{constants.FAIL}\'{repo_name}\' is not a valid repository{constants.ENDC}')
        exit(1)

    else:
        print(f'{constants.OKGREEN} [Done]{constants.ENDC}')

    # Get repository
    repo = git.Repo(repository_dir)

    return repo

def get_branches(repository):
    """
    Gets branches from a github repository. Filters out unwanted branches
    """
    # Get all branches
    return filter_branches(repository.remote().refs)

def isFullApp(repository):
    """
    Returns true if repository is a full app, false if it is minified.
    Full app determined if branches contain "secure" branch
    """
    is_full_app = False
    branches = get_branches(repository)

    # If full app branch exists, repo is a full app, otherwise it is minified
    if JIRA_FA_SECURE_BRANCH in branches:
        is_full_app = True
    
    return is_full_app

def did_commit_add_or_remove_lines(repository):
    """
    Check if the commit added or removed any lines. Return true if lines were added or removed
    """
    # added_or_removed_lines = False

    # diff = repository.git.diff('--numstat', 'HEAD^').split("\n")

    # for edited_file_stat in diff:
    #     stat = edited_file_stat.split()

    #     if stat[0] == '-':
    #         added = 0
    #     else:
    #         added = int(stat[0])
        
    #     if stat[1] == '-':
    #         removed = 0
    #     else:
    #         removed = stat[1]
        
    #     if added - removed != 0:
    #         added_or_removed_lines = True
        
    # return added_or_removed_lines
    return True