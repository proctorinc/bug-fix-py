import git
import os
import subprocess
from src import constants
from src.constants import colors
from . import utils

class GitRepository:
    """
    Class wrapper around GitPython for git repository functionality 
    """
    def __init__(self, repo_name):
        self.__repository = self.__clone_repository(repo_name)
        self.__repository_dir = self.__get_repository_dir(repo_name)
        self.__branches = utils.retrieve_branches(self.__repository)
        self.__is_full_app = utils.check_is_full_app(self.__branches)
        self.__fix_messages = []
        self.__did_cherrypick = False

    def get_num_branches(self):
        """
        Get the number of branches in this repository
        """
        return len(self.__branches)

    def get_is_full_app(self):
        """
        Get whether the app is minified or full
        """
        return self.__is_full_app

    def get_fix_messages(self):
        """
        Get fix messages created from commits to repo
        """
        return self.__fix_messages

    def did_cherrypick_run(self):
        """
        Return whether cherrypick has been run or not
        """
        # TODO: This value needs to be modified in the cherrypick script!
        return self.__did_cherrypick

    # TODO: fix method functionality
    def did_number_of_lines_change(self):
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

    def push(self):
        """
        Push repository changes to github
        """
        # Push commit to the repository
        subprocess.check_output(f'git -C {self.__repository_dir} push --all', shell=True)

    def __get_repository_dir(self, repo_name):
        """
        Returns absolute url for repository folder
        """
        return os.path.join(constants.GIT_REPO_DIR, repo_name)
        
    def __clone_repository(self, repo_name):
        """
        Clone repository and return valid instance. Handle errors for invalid repository
        """
        git_url = f'{constants.JIRA_SCW_GIT_URL}/{repo_name}.git'
        repository_dir = self.__get_repository_dir(repo_name)

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
            raise ValueError(f'{colors.FAIL}Either \'{repo_name}\' is not a valid repository\nor you do not have the correct rights to access this repo{colors.ENDC}')

        else:
            print(f'{colors.OKGREEN} [Done]{colors.ENDC}')

        # Create repository object
        repo = git.Repo(repository_dir)

        return repo

    def run_bug_fix(self):
        """
        Run bug fix. Loop over branches to fix. After fixing, prompt
        user if they want to fix another
        """
        # Default user is not done fixing branches
        done_fixing = False

        # Set default cherrypick has not occurred
        did_cherrypick = False

        # Hold fix messages for all branches in list
        fix_messages = []

        # Track whether chunks need to be fixed or not
        fix_chunks_required = False

        # Continue to fix branches until user is done
        while not done_fixing:

            ###########
            #
            # Allow user to stop fixing branch at anytime
            #
            ###########

            # Fix the branch and retrieve the name and fix explanation
            fix_message, fixed_branch = utils.fix_and_commit_branch(self.__repository, self.__repository_dir, self.__branches, self.__is_full_app)

            # Remove initial_branch from branches to avoid cherry-picking it
            self.__branches.remove(fixed_branch)

            # Add message to list of messages
            fix_messages.append(fix_message)

            # Keep track of chunks needing to be fixed
            if utils.did_commit_add_or_remove_lines(self.__repository):
                fix_chunks_required = True

            # If full app and fix was on the secure branch, cherry-pick branches
            if self.__is_full_app and fixed_branch == constants.JIRA_FA_SECURE_BRANCH:

                # Get the commit ID
                commit_id = self.__repository.rev_parse('HEAD')

                # Run cherry-pick method
                utils.cherrypick(self.__repository_dir, self.__branches, commit_id)

                # Confirm that cherrypick occurred
                did_cherrypick = True

            # Prompt user to fix another branch
            fix_branch = input(f'\nFix another branch? (y/{colors.BOLD}{colors.WHITE}N{colors.ENDC}){colors.ENDC}: {colors.WHITE}')

            print(colors.ENDC, end='')

            # If not yes, user is done fixing
            if fix_branch != 'y':
                done_fixing = True