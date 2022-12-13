from dataclasses import dataclass

from bugfixpy.jira.issue import ApplicationCreationIssue, ChallengeCreationIssue


@dataclass
class ChallengeScreenData:
    application_endpoint: str
    chlc: ChallengeCreationIssue


@dataclass
class ApplicationScreenData:
    chlc: ApplicationCreationIssue
    repository_name: str


@dataclass
class ScraperData:
    challenge: ChallengeScreenData
    application: ApplicationScreenData
