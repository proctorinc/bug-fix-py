import re

import requests
from bs4 import BeautifulSoup
from requests import Response
from src import constants


def get_soup(result: Response) -> BeautifulSoup:
    """
    Returns result content turned into Beautiful Soup object
    """
    return BeautifulSoup(result.content, "html.parser")


def get_challenge_chlc(result: Response) -> str:
    """
    Get the value of the challenge CHLC that is located in a link
    that contains SCW's base Jira url
    """
    return get_value_from_link(result, constants.JIRA_SCW_BROWSE_URL)


def get_git_repository(result: Response) -> str:
    """
    Get the value of the Github repository that is located in a link
    that contains SCW's base Github url
    """
    return get_value_from_link(result, constants.GIT_SCW_CONTENT_URL)


def get_value_from_link(result: Response, url_pattern: str) -> str:
    """
    Searches all links on page and returns the value after the url pattern in the href
    """
    soup = get_soup(result)
    links = soup.findAll("a", href=True)

    for link in links:
        href = link["href"]
        if url_pattern in href:
            return href.split(url_pattern)[1]

    return ""


def get_application_endpoint(result: Response) -> str:
    """
    Searches all links on the page for the applications/id/show url
    """
    soup = get_soup(result)
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
    soup = get_soup(result)
    csrf_token = str(soup.find("input", {"name": "_csrf_token"}).get("value"))

    return csrf_token


def did_login_fail(result: requests.models.Response) -> bool:
    """
    Checks if login failed based off of error message existing. Post request always returns 200,
    so scraping to check if login failed is needed.
    """
    soup = get_soup(result)
    login_failed = bool(
        soup.find_all(
            "div", {"class": "alert alert-danger alert-dismissible fade show"}
        )
    )

    return login_failed
