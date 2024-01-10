import re
from typing import Optional
from requests import Session, Response

from bugfixpy.exceptions import RequestFailedError
from bugfixpy.utils import validate

from .scraper_data import (
    ApplicationScreenData,
    ApplicationScreenDataWithChallengeBranches,
    ChallengeScreenData,
    ScraperData,
)
from . import soup_parser
from . import constants


class CmsScraper:
    __session: Session
    __email: Optional[str]
    __password: Optional[str]

    def __init__(
        self,
    ) -> None:
        self.__session = Session()
        self.__email = constants.EMAIL
        self.__password = constants.PASSWORD
        self.login_to_cms()

    def __del__(self) -> None:
        self.__session.close()

    def scrape_challenge_data(self, challenge_id: str) -> ScraperData:
        if not validate.is_valid_challenge_id(challenge_id):
            raise ValueError(f"Invalid challenge_id: {challenge_id}")

        challenge_screen_data = self.scrape_challenge_screen(challenge_id)

        application_screen_data = (
            self.scrape_application_data_with_challenge_map_by_url(
                challenge_screen_data.application_endpoint
            )
        )

        return ScraperData(challenge_screen_data, application_screen_data)

    def scrape_application_data(self, application_name: str) -> ApplicationScreenData:
        if not validate.is_valid_application_name(application_name):
            raise ValueError(f"Invalid application name: {application_name}")

        application_data = self.scrape_application_screen_by_name(application_name)

        return application_data

    def scrape_application_data_with_challenge_map(
        self, application_name_or_url: str
    ) -> ApplicationScreenDataWithChallengeBranches:
        # if validate.is_valid_application_url(application_name_or_url):
        #     parsed_url = (
        #         application_name_or_url.split("cms.securecodewarrior.com")[0]
        #         if "cms.securecodewarrior.com" in application_name_or_url
        #         else application_name_or_url
        #     )
        #     application_data = self.scrape_application_screen_by_url(parsed_url)
        if validate.is_valid_application_name(application_name_or_url):
            application_data = self.scrape_application_screen_by_name(
                application_name_or_url
            )
        else:
            raise ValueError(f"Invalid application name: {application_name_or_url}")

        return self.parse_application_screen_with_challenge_branches_response(
            application_data
        )

    def scrape_application_data_with_challenge_map_by_url(
        self, application_url: str
    ) -> ApplicationScreenDataWithChallengeBranches:
        application_data = self.scrape_application_screen_by_url(application_url)

        return self.parse_application_screen_with_challenge_branches_response(
            application_data
        )

    def update_branches_for_application(self, application_endpoint) -> None:
        update_endpoint = self.get_update_endpoint(application_endpoint)
        result = self.__session.post(f"{constants.URL}{update_endpoint}")

        if not result.ok:
            raise RequestFailedError("Scraper Error: scraping application page failed")

    def get_update_endpoint(self, application_endpoint) -> str:
        return application_endpoint.replace("show", "update-branches")

    def login_to_cms(self) -> None:
        csrf_token = self.fetch_csrf_token()

        response = self.send_login_request(csrf_token)

        if self.did_login_fail(response):
            raise RequestFailedError(
                "Scraper Error: Failed to login to CMS. Incorrect credentials"
            )

    def fetch_csrf_token(self) -> str:
        response = self.create_csrf_token()

        return self.parse_csrf_token_from_response(response)

    def create_csrf_token(self) -> Response:
        response = self.__session.get(constants.LOGIN_URL)

        if not response.ok:
            raise RequestFailedError("Scraper Error: Failed to fetch CSRF token")

        return response

    def parse_csrf_token_from_response(self, response) -> str:
        return soup_parser.parse_csrf_token(response)

    def send_login_request(self, csrf_token) -> Response:
        payload = {
            "_username": self.__email,
            "_password": self.__password,
            "_csrf_token": csrf_token,
        }

        response = self.__session.post(
            constants.LOGIN_URL,
            data=payload,
        )

        return response

    def did_login_fail(self, response) -> bool:
        return soup_parser.did_login_fail(response)

    def scrape_challenge_screen(self, challenge_id: str) -> ChallengeScreenData:
        response = self.get_cms_page_by_query_string(challenge_id)

        return self.parse_challenge_screen_response(response)

    def scrape_application_screen_by_name(
        self, application_name
    ) -> ApplicationScreenData:
        url_response = self.get_cms_page_by_query_string(application_name)
        url_endpoint = url_response.url[33:] + "/show"

        if not validate.is_valid_application_url(url_endpoint):
            match = re.search(
                r"/applications/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                url_response.text,
            )
            if match:
                url_endpoint = match.group(0) + "/show"

        response = self.get_application_screen_by_url(url_endpoint)

        return self.parse_application_screen_response(response)

    def scrape_application_screen_by_url(
        self, application_url: str
    ) -> ApplicationScreenData:
        response = self.get_application_screen_by_url(application_url)

        return self.parse_application_screen_response(response)

    def get_cms_page_by_query_string(self, query: str) -> Response:
        result = self.__session.get(f"{constants.SEARCH_URL}?q={query}")

        if not result.content:
            raise RequestFailedError("Scraper Error: scraping application page failed")

        return result

    def get_application_screen_by_url(self, application_url: str) -> Response:
        response = self.__session.get(f"{constants.URL}{application_url}")

        if not response.ok:
            raise RequestFailedError("Scraper Error: scraping application page failed")

        return response

    def get_challenge_screen_by_url(self, challenge_url: str):
        response = self.__session.get(f"{constants.URL}{challenge_url}")

        if not response.ok:
            raise RequestFailedError(
                f"Scraper Error: scraping challenge '{challenge_url}' failed"
            )

        return response

    def parse_challenge_screen_response(self, response) -> ChallengeScreenData:
        return soup_parser.parse_challenge_screen_data(response)

    def parse_application_screen_response(self, response) -> ApplicationScreenData:
        return soup_parser.parse_application_screen_data(response)

    def parse_application_screen_with_challenge_branches_response(
        self, application_data: ApplicationScreenData
    ) -> ApplicationScreenDataWithChallengeBranches:
        challenge_map = {}

        for challenge in application_data.challenges:
            response = self.get_challenge_screen_by_url(challenge.url)

            challenge_data = self.parse_challenge_screen_response(response)

            challenge.vulnerable_branches = challenge_data.vulnerable_branches
            challenge.secure_branch = challenge_data.secure_branch

            challenge_map[challenge.name] = challenge

        return ApplicationScreenDataWithChallengeBranches(
            application_data.chlc,
            application_data.repository_name,
            application_data.challenges,
            challenge_map,
        )
