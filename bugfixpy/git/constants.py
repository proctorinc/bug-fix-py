import os

SCW_CONTENT_URL = "https://github.com/SCWContent/"

REPO_DIR = os.path.join(os.path.dirname(__file__), "../../data/repos")

SCW_GIT_URL = "git@github.com:SCWContent"

FULL_APP_SECURE_BRANCH = "secure"

IGNORE_BRANCHES = {"HEAD", "master", "review", "main", "temp", "empty"}
