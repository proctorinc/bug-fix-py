from dataclasses import dataclass

from bugfixpy.jira import ApplicationCreationIssue, ChallengeCreationIssue
from bugfixpy.utils.text import colors


@dataclass
class ChallengeScreenData:
    application_endpoint: str
    chlc: ChallengeCreationIssue
    secure_branch: str
    vulnerable_branches: list[str]


@dataclass
class Challenge:
    name: str
    url: str
    secure_branch: str
    vulnerable_branches: list[str]

    def __init__(
        self, name=None, url=None, secure_branch=None, vulnerable_branches=None
    ) -> None:
        if name:
            self.name = name
        else:
            self.name = ""
        if url:
            self.url = url
        else:
            self.url = ""
        if secure_branch:
            self.secure_branch = secure_branch
        else:
            self.secure_branch = ""
        if vulnerable_branches:
            self.vulnerable_branches = vulnerable_branches
        else:
            self.vulnerable_branches = []


@dataclass
class ApplicationScreenData:
    def __init__(self, chlc=None, repository_name=None, challenges=None) -> None:
        if chlc:
            self.chlc = chlc
        if repository_name:
            self.repository_name = repository_name
        if challenges:
            self.challenges = challenges

    chlc: ApplicationCreationIssue
    repository_name: str
    challenges: list[Challenge]


@dataclass
class ApplicationScreenDataWithChallengeBranches:
    def __init__(
        self,
        chlc=None,
        repository_name=None,
        challenges=None,
        challenge_map=None,
    ) -> None:
        if chlc:
            self.chlc = chlc
        if repository_name:
            self.repository_name = repository_name
        if challenges:
            self.challenges = challenges
        if challenge_map:
            self.challenge_map = challenge_map

    chlc: ApplicationCreationIssue
    repository_name: str
    challenges: list[str]
    challenge_map: dict[str, Challenge]


@dataclass
class ScraperData:
    challenge: ChallengeScreenData
    application: ApplicationScreenData

    def __init__(
        self,
        challenge=None,
        application=None,
    ) -> None:
        if challenge:
            self.challenge = challenge
        if application:
            self.application = application

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
