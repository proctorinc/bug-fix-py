from dataclasses import dataclass

from bugfixpy.jira.issue import ApplicationCreationIssue, ChallengeCreationIssue
from bugfixpy.utils.text import colors


@dataclass
class ChallengeScreenData:
    application_endpoint: str
    chlc: ChallengeCreationIssue


@dataclass
class ApplicationScreenData:
    chlc: ApplicationCreationIssue
    repository_name: str
    branches: list[str]


@dataclass
class ScraperData:
    challenge: ChallengeScreenData
    application: ApplicationScreenData

    def __str__(self) -> str:
        challenge_issue_id = self.challenge.chlc.get_issue_id()
        application_issue_id = self.application.chlc.get_issue_id()
        repository_name = self.application.repository_name
        challenge_chlc = (
            f"Challenge CHLC: {colors.OKCYAN}{challenge_issue_id}{colors.ENDC}"
        )
        application_chlc = (
            f"Application CHLC: {colors.OKCYAN}{application_issue_id}{colors.ENDC}"
        )
        repository_name = f"Repo: {colors.OKCYAN}{repository_name}{colors.ENDC}"
        return f"{challenge_chlc}\n{application_chlc}\n{repository_name}"
