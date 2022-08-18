"""
Soup parsing module contains methods to scrape data from CMS challenge and application screens
"""

import re
from bs4 import BeautifulSoup
from requests import Response
from bugfixpy.constants import git, jira
from bugfixpy.scraper.scraper_data import ApplicationScreenData, ChallengeScreenData


def __create_soup(result: Response) -> BeautifulSoup:
    """
    Returns result content turned into Beautiful Soup object
    """
    return BeautifulSoup(result.content, "html.parser")


def __parse_chlc_number(soup: BeautifulSoup) -> str:
    """
    Get the value of the challenge CHLC that is located in a link that contains SCW's base Jira url
    """
    return __parse_value_from_link(soup, jira.SCW_BROWSE_URL)


def __parse_git_repository(soup: BeautifulSoup) -> str:
    """
    Get the value of the Github repository that is located in a link that contains SCW's base
    Github url
    """
    return __parse_value_from_link(soup, git.SCW_CONTENT_URL)


def __parse_value_from_link(soup: BeautifulSoup, url_pattern: str) -> str:
    """
    Searches all links on page and returns the value after the url pattern in the href
    """
    links = soup.findAll("a", href=True)

    for link in links:
        href = link["href"]
        if url_pattern in href:
            return href.split(url_pattern)[1]

    return ""


def __parse_application_endpoint(soup: BeautifulSoup) -> str:
    """
    Searches all links on the page for the applications/id/show url
    """
    links = soup.findAll("a", href=True)
    for link in links:
        href = link["href"]
        if re.search("/show$", href):
            return href

    return ""


def parse_csrf_token(result: Response) -> str:
    """
    Parses CSRF token from CMS login page using beautiful soup
    """
    soup = __create_soup(result)

    # Find input for csrf token
    csrf_input = soup.find("input", {"name": "_csrf_token"})

    # Get csrf token value from input
    csrf_token = str(csrf_input.get("value"))

    return csrf_token


def did_login_fail(result: Response) -> bool:
    """
    Checks if login failed based off of error message existing. Post request always returns 200,
    so scraping to check if login failed is needed.
    """
    soup = __create_soup(result)

    login_failed = bool(
        soup.find_all(
            "div", {"class": "alert alert-danger alert-dismissible fade show"}
        )
    )

    return login_failed


def parse_challenge_screen_data(result: Response) -> ChallengeScreenData:
    """
    Parses challenge screen data from CMS login page using beautiful soup
    """
    soup = __create_soup(result)
    challenge_chlc = __parse_chlc_number(soup)
    application_screen_endpoint = __parse_application_endpoint(soup)

    return ChallengeScreenData(application_screen_endpoint, challenge_chlc)


def parse_application_screen_data(result: Response) -> ApplicationScreenData:
    """
    Parses application screen data from CMS login page using beautiful soup
    """
    soup = __create_soup(result)

    application_chlc = __parse_chlc_number(soup)
    repository_name = __parse_git_repository(soup)

    return ApplicationScreenData(application_chlc, repository_name)
