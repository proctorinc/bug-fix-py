from typing import Tuple, Optional
from requests import Session

from bugfixpy.exceptions import RequestFailedError
from bugfixpy.constants import cms
from bugfixpy.utils import validate

from .scraper_data import ApplicationScreenData, ChallengeScreenData, ScraperData
from . import soup_parser


class CmsScraper:
    __session: Session
    __challenge_id: Optional[str]

    def __init__(
        self,
        challenge_id: Optional[str] = None,
        credentials: Optional[Tuple[str, str]] = None,
    ) -> None:
        self.__session = Session()
        self.__credentials = credentials if credentials else (cms.EMAIL, cms.PASSWORD)
        self.__challenge_id = challenge_id

    def __del__(self) -> None:
        self.__session.close()

    @classmethod
    def scrape_challenge_data(cls, challenge_id) -> ScraperData:

        if not validate.is_valid_challenge_id(challenge_id):
            raise ValueError(f"Invalid challenge_id: {challenge_id}")

        scraper = cls(challenge_id)

        scraper.login_to_cms()

        challenge_screen_data = scraper.scrape_challenge_screen()

        application_screen_data = scraper.scrape_application_screen(
            challenge_screen_data.application_endpoint
        )

        return ScraperData(challenge_screen_data, application_screen_data)

    def fetch_csrf_token(self) -> str:
        result = self.__session.get(cms.LOGIN_URL)

        if not result.ok:
            raise RequestFailedError("Scraper Error: Failed to fetch CSRF token")

        csrf_token = soup_parser.parse_csrf_token(result)

        return csrf_token

    def login_to_cms(self) -> None:
        email, password = self.__credentials

        csrf_token = self.fetch_csrf_token()

        payload = {
            "_username": email,
            "_password": password,
            "_csrf_token": csrf_token,
        }

        result = self.__session.post(
            cms.LOGIN_URL,
            data=payload,
        )

        login_failed = soup_parser.did_login_fail(result)

        if login_failed:
            raise RequestFailedError(
                "Scraper Error: Failed to login to CMS. Incorrect credentials"
            )

    def scrape_challenge_screen(self) -> ChallengeScreenData:
        result = self.__session.get(f"{cms.SEARCH_URL}?q={self.__challenge_id}")

        if not result.content:
            raise RequestFailedError("Scraper Error: scraping application page failed")

        return soup_parser.parse_challenge_screen_data(result)

    def scrape_application_screen(
        self, application_endpoint: str
    ) -> ApplicationScreenData:
        result = self.__session.get(f"{cms.URL}{application_endpoint}")

        if not result.ok:
            raise RequestFailedError("Scraper Error: scraping application page failed")

        return soup_parser.parse_application_screen_data(result)
