import re
from bs4 import BeautifulSoup
from requests import Response

from bugfixpy.constants import git, jira
from bugfixpy.jira.issue import ApplicationCreationIssue, ChallengeCreationIssue
from bugfixpy.scraper.scraper_data import ApplicationScreenData, ChallengeScreenData


def __create_soup(result: Response) -> BeautifulSoup:
    return BeautifulSoup(result.content, "html.parser")


def __parse_chlc_number(soup: BeautifulSoup) -> str:
    return __parse_value_from_link(soup, jira.SCW_BROWSE_URL)


def __parse_git_repository(soup: BeautifulSoup) -> str:
    return __parse_value_from_link(soup, git.SCW_CONTENT_URL)


def __parse_value_from_link(soup: BeautifulSoup, url_pattern: str) -> str:
    links = soup.findAll("a", href=True)

    for link in links:
        href = link["href"]
        if url_pattern in href:
            return href.split(url_pattern)[1]

    return ""


def __parse_application_endpoint(soup: BeautifulSoup) -> str:
    links = soup.findAll("a", href=True)
    for link in links:
        href = link["href"]
        if re.search("/show$", href):
            return href

    return ""


def parse_csrf_token(result: Response) -> str:
    soup = __create_soup(result)

    # Find input for csrf token
    csrf_input = soup.find("input", {"name": "_csrf_token"})

    # Get csrf token value from input
    csrf_token = str(csrf_input.get("value"))

    return csrf_token


def did_login_fail(result: Response) -> bool:
    soup = __create_soup(result)

    login_failed = bool(
        soup.find_all(
            "div", {"class": "alert alert-danger alert-dismissible fade show"}
        )
    )

    return login_failed


def parse_challenge_screen_data(result: Response) -> ChallengeScreenData:
    soup = __create_soup(result)
    challenge_creation_number = __parse_chlc_number(soup)
    application_screen_endpoint = __parse_application_endpoint(soup)

    return ChallengeScreenData(
        application_screen_endpoint, ChallengeCreationIssue(challenge_creation_number)
    )


def parse_application_screen_data(result: Response) -> ApplicationScreenData:
    soup = __create_soup(result)

    application_creation_number = __parse_chlc_number(soup)
    repository_name = __parse_git_repository(soup)

    return ApplicationScreenData(
        ApplicationCreationIssue(application_creation_number), repository_name
    )
