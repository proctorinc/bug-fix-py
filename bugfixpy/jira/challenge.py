"""Challenge class"""
from bugfixpy.jira import (
    ChallengeRequestIssue,
    ChallengeCreationIssue,
    ApplicationCreationIssue,
)


class Challenge:
    """Class Representation of an SCW Challenge"""

    __challenge_request_issue: ChallengeRequestIssue
    __challenge_creation_issue: ChallengeCreationIssue
    __application_creation_issue: ApplicationCreationIssue

    def get_challenge_request_issue(self) -> ChallengeRequestIssue:
        return self.__challenge_request_issue

    def get_challenge_creation_issue(self) -> ChallengeCreationIssue:
        return self.__challenge_creation_issue

    def get_application_creation_issue(self) -> ApplicationCreationIssue:
        return self.__application_creation_issue
