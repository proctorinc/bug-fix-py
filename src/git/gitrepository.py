import git
import os
import subprocess
from src import constants
from . import utils

class GitRepository:
    """
    Class wrapper around GitPython for git repository functionality 
    """
    def __init__(self, repo_name):
        self.__repository = self.__clone_repository(repo_name)
        self.__branches = utils.retrieve_branches(self.__repository)
        self.__is_full_app = utils.is_full_app(self.__branches)

    def get_repository(self):
        return self.__repository

    def get_num_branches(self):
        return len(self.__branches)

    def get_is_full_app(self):
        return self.__is_full_app

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
            raise ValueError(f'{constants.FAIL}Either \'{repo_name}\' is not a valid repository\nor you do not have the correct rights to access this repo{constants.ENDC}')

        else:
            print(f'{constants.OKGREEN} [Done]{constants.ENDC}')

        # Create repository object
        repo = git.Repo(repository_dir)

        return repo