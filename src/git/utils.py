from src import constants

def filter_branches(remote_refs): # only used here
    """
    Parse branches from remote refs and remove unwanted branches
    """
    filtered_branches = []

    # Loop over remote references
    for refs in remote_refs:

        # Remove origin/ from branch name
        branch = refs.name.split("origin/",1)[1]

        # Filter branches
        if branch not in constants.JIRA_IGNORE_BRANCHES:
            filtered_branches.append(branch)

    return filtered_branches

def retrieve_branches(repository): # used in bugfix main
    """
    Gets branches from a github repository. Filters out unwanted branches
    """
    # Get all branches
    return filter_branches(repository.remote().refs)

#
# Need a better implementation of this using the scraper. This method is not reliable
#

def is_full_app(branches): # used in bugfix main
    """
    Returns true if repository is a full app, false if it is minified.
    Full app determined if branches contain "secure" branch
    """
    is_full_app = False

    # If full app branch exists, repo is a full app, otherwise it is minified
    if constants.JIRA_FA_SECURE_BRANCH in branches:
        is_full_app = True
    
    return is_full_app

#
# This method does not work at all
#

def did_commit_add_or_remove_lines(repository): # used in bugfix main
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