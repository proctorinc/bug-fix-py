import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

# Email to access Jira API
API_EMAIL = os.getenv('API_EMAIL')

# Jira API key
API_KEY = os.getenv('API_KEY')

# Create authentication object for API calls
AUTH = HTTPBasicAuth(API_EMAIL, API_KEY)

# Directory to where the repositories exist
REPO_DIR = './repos/'

# Branches to ignore
IGNORE_BRANCHES = {'HEAD', 'master', 'review', 'main', 'temp' }

# SCW Content Github Url
SCW_GIT_URL = 'git@github.com:SCWContent'

# Full app secure branch name
FA_SECURE_BRANCH = 'secure'

# Thomas account id to link in jira
THOMAS_ACCT_ID = '5bcd95bc3aa82432ce729fcf'

# API defined headers
HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Transition id for planned workflow
TRANSITION_PLANNED = 281

# Transition id for in progress workflow
TRANSITION_IN_PROGRESS = 291
