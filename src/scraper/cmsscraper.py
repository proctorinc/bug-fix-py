import requests
from requests.cookies import RequestsCookieJar
from src import constants, exceptions

from . import utils


class CmsScraper:
    """
    Simple webscraper that scrapes data from the CMS
    """

    __session: requests.Session
    __challenge_id: int
    __challenge_chlc: str
    __application_chlc: str
    __git_repo_name: str

    def __init__(self, challenge_id: int) -> None:
        self.__session = requests.Session()
        self.__challenge_id = challenge_id
        self.__challenge_chlc = ""
        self.__application_chlc = ""
        self.__git_repo_name = ""
        self.__scrape_cms()

    def get_challenge_chlc(self) -> str:
        """
        Gets challenge chlc
        """
        return self.__challenge_chlc

    def get_application_chlc(self) -> str:
        """
        Gets application chlc
        """
        return self.__application_chlc

    def get_git_repo(self) -> str:
        """
        Gets git repository name
        """
        return self.__git_repo_name

    def validate_credentials(self) -> bool:
        """
        Returns whether credentials are valid or not
        """
        return True

    def __scrape_cms(self):
        """
        Scrapes the cms to retrieve
        """
        # Get CSRF token for login
        csrf_token = self.__fetch_csrf_token()

        # Retrieve cookies from logging into the CMS
        cookies = self.__login_to_cms(csrf_token)

        # Scrape the challenge screen and return application endpoint
        application_endpoint = self.__scrape_challenge_screen(cookies)

        self.__scrape_application_screen(cookies, application_endpoint)

    def __fetch_csrf_token(self) -> str:
        """
        Get request to retrieve the CSRF token for logging in
        """
        # Get csrf token and cookies
        result = self.__session.get(constants.CMS_LOGIN_URL)

        # Check if result was successful
        if not result.ok:
            raise exceptions.RequestFailedError(
                "Scraper Error: Failed to fetch CSRF token"
            )

        csrf_token = utils.parse_csrf_token(result)

        return csrf_token

    def __login_to_cms(self, csrf_token: str) -> RequestsCookieJar:
        """
        Login to the CMS using the CSRF token and return cookies for scraping
        """
        # Create the login payload
        payload = {
            "_username": constants.CMS_EMAIL,
            "_password": constants.CMS_PASSWORD,
            "_csrf_token": csrf_token,
        }

        # Login to CMS
        result = self.__session.post(
            constants.CMS_LOGIN_URL,
            data=payload,
        )

        # Check if login failed
        login_failed = utils.did_login_fail(result)

        # Check if login was successful
        if login_failed:
            raise exceptions.RequestFailedError(
                "Scraper Error: Failed to login to CMS. Incorrect credentials"
            )

        return result.cookies

    def __scrape_challenge_screen(self, cookies: RequestsCookieJar):
        """
        Get request to search for challenge id. Scrape challenge screen.
        Retrieve challenge CHLC and application screen endpoint.
        """
        result = self.__session.get(
            f"{constants.CMS_SEARCH_URL}?q={self.__challenge_id}", cookies=cookies
        )

        # Check if searching for challenge was successful
        if not result.content:
            raise exceptions.RequestFailedError(
                "Scraper Error: scraping application page failed"
            )

        # Initialize Challenge CHLC
        self.__challenge_chlc = utils.get_challenge_chlc(result)

        # Get application page url
        application_endpoint = utils.get_application_endpoint(result)

        return application_endpoint

    def __scrape_application_screen(
        self, cookies: RequestsCookieJar, application_endpoint: str
    ):
        """
        Get request to retrieve application screen. Scrape the screen to
        retrieve application CHLC and github repository name.
        """
        # Query application page
        result = self.__session.get(
            f"{constants.CMS_URL}{application_endpoint}", cookies=cookies
        )

        # Check if requesting application page was successful
        if not result.ok:
            raise exceptions.RequestFailedError(
                "Scraper Error: scraping application page failed"
            )

        # Initialize Application CHLC
        self.__application_chlc = utils.get_challenge_chlc(result)

        # Initialize Github repository name
        self.__git_repo_name = utils.get_git_repository(result)
