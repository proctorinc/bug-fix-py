import git
import os
import subprocess

from text import Colors

from constants import (
    IGNORE_BRANCHES,
    SCW_GIT_URL,
    REPO_DIR,
    FA_SECURE_BRANCH
)

def filterRefs(remote_refs):
    """
    Parse branches from remote refs and remove unwanted branches
    """
    branches = []

    # Loop over remote references
    for refs in remote_refs:

        # Remove origin/ from branch name
        branch = refs.name.split("origin/",1)[1]

        # Filter branches
        if branch not in IGNORE_BRANCHES:
            branches.append(branch)

    return branches

def getRepositoryURL(repo_name):
    """
    Returns absolute url for repository folder
    """
    return os.path.join(REPO_DIR, repo_name)

def cloneRepository(repo_name):
    """
    Clone repository and return valid instance. Handle errors for invalid repository
    """
    git_url = f'{SCW_GIT_URL}/{repo_name}.git'
    repository_url = getRepositoryURL(repo_name)

    print(f'Cloning Repository...', end='')

    # If repo folder already exists, remove it
    if os.path.isdir(repository_url):
        
        # Alert user of repo existing
        print(f'\nRepository cached. Resetting...', end='')

        # Delete repository
        subprocess.check_output(f'sudo rm -r {repository_url}', shell=True)
    try:
        # Clone repository
        git.Repo.clone_from(git_url, repository_url)
    
    except git.exc.GitError:
        print(f'{Colors.FAIL}\'{repo_name}\' is not a valid repository{Colors.ENDC}')
        exit(1)

    else:
        print(f'{Colors.OKGREEN} [Done]{Colors.ENDC}')

    # Get repository
    repo = git.Repo(repository_url)

    return repo

def getBranches(repository):
    """
    Gets branches from a github repository. Filters out unwanted branches
    """
    # Get all branches
    return filterRefs(repository.remote().refs)

def isFullApp(repository):
    """
    Returns true if repository is a full app, false if it is minified.
    Full app determined if branches contain "secure" branch
    """
    is_full_app = False
    branches = getBranches(repository)

    # If full app branch exists, repo is a full app, otherwise it is minified
    if FA_SECURE_BRANCH in branches:
        is_full_app = True
    
    return is_full_app

def commitAddedOrRemovedLines(repository):
    """
    Check if the commit added or removed any lines. Return true if lines were added or removed
    """
    added_or_removed_lines = False

    diff = repository.git.diff('--numstat', 'HEAD^').split("\n")

    for edited_file_stat in diff:
        stat = edited_file_stat.split()

        if int(stat[0]) - int(stat[1]) != 0:
            added_or_removed_lines = True
        
    return added_or_removed_lines