from dataclasses import dataclass


@dataclass
class ChallengeScreenData:
    """
    Models data scraped from CMS challenge screen
    """

    application_endpoint: str
    chlc: str


@dataclass
class ApplicationScreenData:
    """
    Models data scraped from CMS application screen
    """

    chlc: str
    repository_name: str


@dataclass
class ScraperData:
    """
    Models data retrieved from CMS scraper
    """

    challenge: ChallengeScreenData
    application: ApplicationScreenData
