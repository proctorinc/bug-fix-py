from typing import Optional
from requests import Session, Response

from bugfixpy.exceptions import RequestFailedError
from bugfixpy.constants import cms
from bugfixpy.utils import validate

from .scraper_data import ApplicationScreenData, ChallengeScreenData, ScraperData
from . import soup_parser


class CmsScraper:
    __session: Session
    __challenge_id: Optional[str]
    __email: Optional[str]
    __password: Optional[str]

    def __init__(
        self,
        challenge_id: Optional[str] = None,
    ) -> None:

        if not validate.is_valid_challenge_id(challenge_id):
            raise ValueError(f"Invalid challenge_id: {challenge_id}")

        self.__session = Session()
        self.__email = cms.EMAIL
        self.__password = cms.PASSWORD
        self.__challenge_id = challenge_id

        print(self.__email, self.__password)

    def __del__(self) -> None:
        self.__session.close()

    @classmethod
    def scrape_challenge_data(cls, challenge_id) -> ScraperData:

        scraper = cls(challenge_id)

        scraper.login_to_cms()

        challenge_screen_data = scraper.scrape_challenge_screen()

        application_screen_data = scraper.scrape_application_screen(
            challenge_screen_data.application_endpoint
        )
        print(challenge_screen_data.application_endpoint)

        return ScraperData(challenge_screen_data, application_screen_data)

    def update_branches_for_application(self, application_endpoint) -> None:
        update_endpoint = self.get_update_endpoint(application_endpoint)
        result = self.__session.post(f"{cms.URL}{update_endpoint}")

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
        response = self.__session.get(cms.LOGIN_URL)

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
            cms.LOGIN_URL,
            data=payload,
        )

        return response

    def did_login_fail(self, response) -> bool:
        return soup_parser.did_login_fail(response)

    def scrape_challenge_screen(self) -> ChallengeScreenData:
        response = self.get_challenge_screen_by_id()

        return self.parse_challenge_screen_response(response)

    def scrape_application_screen(self, application_url: str) -> ApplicationScreenData:

        response = self.get_application_screen_by_url(application_url)

        return self.parse_application_screen_response(response)

    def get_challenge_screen_by_id(self) -> Response:
        result = self.__session.get(f"{cms.SEARCH_URL}?q={self.__challenge_id}")

        if not result.content:
            raise RequestFailedError("Scraper Error: scraping application page failed")

        return result

    def get_application_screen_by_url(self, application_url) -> Response:
        response = self.__session.get(f"{cms.URL}{application_url}")

        if not response.ok:
            raise RequestFailedError("Scraper Error: scraping application page failed")

        return response

    def parse_challenge_screen_response(self, response) -> ChallengeScreenData:
        return soup_parser.parse_challenge_screen_data(response)

    def parse_application_screen_response(self, response) -> ApplicationScreenData:
        return soup_parser.parse_application_screen_data(response)
