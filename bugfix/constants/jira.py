import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

######################
# JIRA API Constants #
######################

# Email to access Jira API
JIRA_API_EMAIL = os.getenv('JIRA_API_EMAIL')

# Jira API key
JIRA_API_KEY = os.getenv('JIRA_API_KEY')

# Create authentication object for API calls
JIRA_AUTH = HTTPBasicAuth(JIRA_API_EMAIL, JIRA_API_KEY)

# Directory to where the repositories exist
JIRA_REPO_DIR = '../repos/'

# Branches to ignore
JIRA_IGNORE_BRANCHES = {'HEAD', 'master', 'review', 'main', 'temp' }

# SCW Content Github Url
JIRA_SCW_GIT_URL = 'git@github.com:SCWContent'

# Full app secure branch name
JIRA_FA_SECURE_BRANCH = 'secure'

# Thomas account id to link in jira
JIRA_THOMAS_ACCT_ID = '5bcd95bc3aa82432ce729fcf'

# API defined headers
JIRA_REQUEST_HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Jira id for transitioning to "planned" in workflow
JIRA_TRANSITION_PLANNED = 281

# Jira id for transitioning to "in progress" in workflow
JIRA_TRANSITION_IN_PROGRESS = 291