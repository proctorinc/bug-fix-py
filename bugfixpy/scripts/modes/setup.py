"""
Setup mode script runs setup process for credentials for running CMS scraper and Jira API
transitioning. Credentials must exist and be valid to run the automated processe
"""


import sys
from getpass import getpass
from bugfixpy.constants import jira, cms


def run() -> None:
    """
    Setup credentials process. Get user input to change credentials in environment
    """
    api_email = jira.API_EMAIL
    api_key = jira.API_KEY
    cms_email = cms.EMAIL
    cms_password = cms.PASSWORD

    if api_email and api_key and cms_email and cms_password:
        print("All credentials are setup")
        reset_credentials = input("Would you like to reset your credentials? (y/n) ")

        if reset_credentials == "y":
            api_email = None
            api_key = None
            cms_email = None
            cms_password = None
        else:
            sys.exit(0)

    # If jira email does not exist, prompt for it
    while not api_email:
        api_email = input("Enter Jira Email: ")

    # If api key does not exist, prompt for it
    while not api_key:
        print(
            "Get a Jira API key here: https://id.atlassian.com/manage-profile/security/api-tokens"
        )
        api_key = input("Enter Jira API key: ")

    # If CMS email address does not exist, prompt for it
    while not cms_email:
        cms_email = input("Enter CMS Email: ")

    # If CMS password does not exist, prompt for it
    while not cms_password:
        cms_password = getpass(prompt="Enter CMS Password: ")

    # Write credentials to environment
    with open(".env", "w", encoding="utf8") as env:
        env.write(f"JIRA_API_EMAIL={api_email}\n")
        env.write(f"JIRA_API_KEY={api_key}\n")
        env.write(f"CMS_EMAIL={cms_email}\n")
        env.write(f"CMS_PASSWORD={cms_password}\n")

    # TODO: ADD VALIDATIONS FOR CMS CREDENTIALS
    # TODO: validate credentials after you get them!
    # if jira_api.has_valid_credentials(api_email, api_key):
    # print("Jira API Credentials are valid.")
    # print("Run program: python3 bugfixpy")
    print("Warning, function not finished!")

    sys.exit(0)
