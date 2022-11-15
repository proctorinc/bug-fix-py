"""Challenge class"""
from dataclasses import dataclass
from bugfixpy.jira import (
    ChallengeRequestIssue,
    ChallengeCreationIssue,
    ApplicationCreationIssue,
)


@dataclass
class Challenge:
    challenge_request_issue: ChallengeRequestIssue
    challenge_creation_issue: ChallengeCreationIssue
    application_creation_issue: ApplicationCreationIssue
