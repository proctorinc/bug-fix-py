"""
CMS Scraper class scrapes the CMS challenge and application screens which requires collecting a
CSRF token, logging into the CMS, and scraping data. Uses scraper data classes to define what is
returned from the challenge and application screens.
"""


from typing import Tuple, Optional
from requests import Session
from bugfixpy.exceptions import RequestFailedError
from bugfixpy.constants import cms
from bugfixpy.utils import validate
from .scraper_data import ApplicationScreenData, ChallengeScreenData
from . import soup_parser


class CmsScraper:
    """Simple webscraper that scrapes data from the CMS"""

    __session: Session
    __challenge_id: str

    def __init__(
        self, challenge_id: str, credentials: Optional[Tuple[str, str]] = None
    ) -> None:
        self.__session = Session()
        self.__challenge_id = challenge_id
        self.__credentials = credentials if credentials else (cms.EMAIL, cms.PASSWORD)

        if not validate.is_valid_challenge_id(challenge_id):
            raise ValueError(f"Invalid challenge_id: {challenge_id}")

    def __del__(self) -> None:
        """On destruction of object, close the scraper session"""

        self.__session.close()

    def fetch_csrf_token(self) -> str:
        """Get request to retrieve the CSRF token for logging in"""

        # Get csrf token and cookies
        result = self.__session.get(cms.LOGIN_URL)

        # Check if result was successful
        if not result.ok:
            raise RequestFailedError("Scraper Error: Failed to fetch CSRF token")

        csrf_token = soup_parser.parse_csrf_token(result)

        return csrf_token

    def login_to_cms(self, csrf_token: str) -> None:
        """Login to the CMS using the CSRF token and return cookies for scraping"""

        email, password = self.__credentials

        # Create the login payload
        payload = {
            "_username": email,
            "_password": password,
            "_csrf_token": csrf_token,
        }

        # Login to CMS
        result = self.__session.post(
            cms.LOGIN_URL,
            data=payload,
        )

        # Check if login failed
        login_failed = soup_parser.did_login_fail(result)

        # Check if login was successful
        if login_failed:
            raise RequestFailedError(
                "Scraper Error: Failed to login to CMS. Incorrect credentials"
            )

    def scrape_challenge_screen(self) -> ChallengeScreenData:
        """
        Get request to search for challenge id. Scrape challenge screen.
        Retrieve challenge CHLC and application screen endpoint.
        """
        result = self.__session.get(f"{cms.SEARCH_URL}?q={self.__challenge_id}")

        # Check if searching for challenge was successful
        if not result.content:
            raise RequestFailedError("Scraper Error: scraping application page failed")

        return soup_parser.parse_challenge_screen_data(result)

    def scrape_application_screen(
        self, application_endpoint: str
    ) -> ApplicationScreenData:
        """
        Get request to retrieve application screen. Scrape the screen to
        retrieve application CHLC and github repository name.
        """
        # Query application page
        result = self.__session.get(f"{cms.URL}{application_endpoint}")

        # Check if requesting application page was successful
        if not result.ok:
            raise RequestFailedError("Scraper Error: scraping application page failed")

        return soup_parser.parse_application_screen_data(result)

    def update_application_branches(self, application_endpoint: str) -> None:
        """Updated the branches for the entire application in the CMS"""

        # Run post request to update the branches for the entire application
        result = self.__session.post(f"{cms.URL}{application_endpoint}")

        # Check if updating branch was successful
        if result.status_code != 200:
            raise RequestFailedError(
                "Scraper Error: updating application branches failed"
            )
