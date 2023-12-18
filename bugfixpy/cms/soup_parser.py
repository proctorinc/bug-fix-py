import re
from bs4 import BeautifulSoup
from requests import Response

from bugfixpy import git, jira
from bugfixpy.jira import ApplicationCreationIssue, ChallengeCreationIssue
from bugfixpy.cms.scraper_data import (
    ApplicationScreenData,
    Challenge,
    ChallengeScreenData,
)


def __create_soup(result: Response) -> BeautifulSoup:
    return BeautifulSoup(result.content, "html.parser")


def __parse_chlc_number(soup: BeautifulSoup) -> str:
    return __parse_value_from_link(soup, jira.constants.SCW_BROWSE_URL)


def __parse_git_repository(soup: BeautifulSoup) -> str:
    return __parse_value_from_link(soup, git.constants.SCW_CONTENT_URL)


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


def __parse_challenge_vulnerable_branches(soup: BeautifulSoup) -> list[str]:
    branches = []

    divs = soup.find_all("i", {"class": "fa fa-code-branch"})

    vulnerable = divs[0].parent.contents[1].strip()
    incorrect_1 = divs[2].parent.contents[1].strip()
    incorrect_2 = divs[3].parent.contents[1].strip()
    incorrect_3 = divs[4].parent.contents[1].strip()

    branches.append(vulnerable)
    branches.append(incorrect_1)
    branches.append(incorrect_2)
    branches.append(incorrect_3)

    return branches


def __parse_challenge_secure_branch(soup: BeautifulSoup) -> str:
    secure_branch = "secure"

    divs = soup.find_all("i", {"class": "fa fa-code-branch"})
    secure_branch = divs[1].parent.contents[1].strip()

    return secure_branch


def __parse_challenges(soup: BeautifulSoup) -> list[Challenge]:
    challenges = []
    tables = soup.findAll("table")
    rows = tables[1].findAll("tr")

    for table_row in rows[1:]:
        cols = table_row.findAll("td")
        link = cols[0].find("a", href=True)
        url = link["href"]
        span = cols[2].find("span")
        name = link.contents[0].strip()
        status = span.contents[0].strip()

        if (
            status != "Deprecated"
            and status != "Cancelled"
            and status != "Todo"
            and status != "Retired"
        ):
            challenges.append(
                Challenge(
                    name,
                    url,
                )
            )

    return challenges


# def __parse_branches(soup: BeautifulSoup) -> list[str]:
#     branches = []
#     tables = soup.findAll("table")
#     rows = tables[1].findAll("tr")

#     for table_row in rows[1:]:
#         cols = table_row.findAll("td")
#         link = cols[0].find("a", href=True)
#         span = cols[2].find("span")
#         name = link.contents[0].strip()
#         status = span.contents[0].strip()

#         if (
#             status != "Deprecated"
#             and status != "Cancelled"
#             and status != "Todo"
#             and status != "Retired"
#         ):
#             # Add branch and all incorrect branches
#             incorrect_zero = name + "_incorrect_0"
#             incorrect_one = name + "_incorrect_1"
#             incorrect_two = name + "_incorrect_2"
#             branches.append(incorrect_zero)
#             branches.append(incorrect_one)
#             branches.append(incorrect_two)

#     return branches


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
    vulnerable_branches = __parse_challenge_vulnerable_branches(soup)
    secure_branch = __parse_challenge_secure_branch(soup)

    return ChallengeScreenData(
        application_screen_endpoint,
        ChallengeCreationIssue(challenge_creation_number),
        secure_branch,
        vulnerable_branches,
    )


def parse_application_screen_data(result: Response) -> ApplicationScreenData:
    soup = __create_soup(result)

    application_creation_number = __parse_chlc_number(soup)
    repository_name = __parse_git_repository(soup)
    challenges = __parse_challenges(soup)

    return ApplicationScreenData(
        ApplicationCreationIssue(application_creation_number),
        repository_name,
        challenges,
    )


def parse_application_screen_with_challenges_data(
    result: Response,
) -> ApplicationScreenData:
    soup = __create_soup(result)

    application_creation_number = __parse_chlc_number(soup)
    repository_name = __parse_git_repository(soup)
    challenges = __parse_challenges(soup)

    return ApplicationScreenData(
        ApplicationCreationIssue(application_creation_number),
        repository_name,
        challenges,
    )
