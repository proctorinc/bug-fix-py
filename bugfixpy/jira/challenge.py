"""Challenge class"""
from bugfixpy.jira import (
    ChallengeRequestIssue,
    ChallengeCreationIssue,
    ApplicationCreationIssue,
)


class Challenge:
    """
    Challenge class
    """

    __challenge_request_issue: ChallengeRequestIssue
    __challenge_creation_issue: ChallengeCreationIssue
    __application_creation_issue: ApplicationCreationIssue

    def get_challenge_request_issue(self):
        """Gets the challenge request issue"""
        return self.__challenge_request_issue

    def get_challenge_creation_issue(self):
        """Gets the challenge creation issue"""
        return self.__challenge_creation_issue

    def get_application_creation_issue(self):
        """Gets the application creation issue"""
        return self.__application_creation_issue
