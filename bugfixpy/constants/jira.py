"""
Jira constants
"""


import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

# Email to access Jira API
API_EMAIL = os.getenv("JIRA_API_EMAIL")

# Jira API key
API_KEY = os.getenv("JIRA_API_KEY")

# Create authentication object for API calls
AUTH = HTTPBasicAuth(API_EMAIL, API_KEY)
# Branches to ignore
IGNORE_BRANCHES = {"HEAD", "master", "review", "main", "temp"}

# SCW Content Github Url
SCW_GIT_URL = "git@github.com:SCWContent"
# Full app secure branch name
FULL_APP_SECURE_BRANCH = "secure"

# Thomas account id to link in jira
THOMAS_ACCT_ID = "5bcd95bc3aa82432ce729fcf"

# API defined headers
REQUEST_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# Jira id for transitioning to "planned" in workflow
TRANSITION_PLANNED = 281

# Jira id for transitioning to "in progress" in workflow
TRANSITION_IN_PROGRESS = 291

# Jira id for transitioning to "feedback open" in workflow
TRANSITION_FEEDBACK_OPEN = 511

# Jira id for transitioning to "feedback review" in workflow
TRANSITION_FEEDBACK_REVIEW = 521

# SCW base URL for Jira browsing
SCW_BROWSE_URL = "https://securecodewarrior.atlassian.net/browse/"

# SCW base URL for Jira API
SCW_API_URL = "https://securecodewarrior.atlassian.net/rest/api/latest"

# API response "key" entry
RESPONSE_KEY = "key"

# CHLRQ string
CHRLQ = "CHLRQ"

# CHLC string
CHLC = "CHLC"

# Bulk transition JQL url
BULK_TRANSITION_JQL_URL = "https://securecodewarrior.atlassian.net/browse/CHLC-{chlc}?jql=project%20%3D%20%27CHLC%27%20and%20issuetype%3D%20challenge%20and%20issue%20in%20linkedIssues(%27CHLC-{chlc}%27)%20ORDER%20BY%20created%20DESC"
