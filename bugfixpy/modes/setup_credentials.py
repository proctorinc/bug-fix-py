import sys
from getpass import getpass
import keyring
from bugfixpy.constants import jira, cms


class SetupCredentials:
    @staticmethod
    def run() -> None:
        api_email = jira.API_EMAIL
        api_key = jira.API_KEY
        cms_email = cms.EMAIL
        cms_password = cms.PASSWORD

        if api_email and api_key and cms_email and cms_password:
            print("All credentials are setup")
            reset_credentials = input(
                "Would you like to reset your credentials? (y/n) "
            )

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

        keyring.set_password("system", "JIRA_API_EMAIL", api_email)
        keyring.set_password("system", "JIRA_API_KEY", api_key)
        keyring.set_password("system", "CMS_EMAIL", cms_email)
        keyring.set_password("system", "CMS_PASSWORD", cms_password)

        print("--setup script is not finished!")

        sys.exit(0)
