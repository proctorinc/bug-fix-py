from bs4 import BeautifulSoup
import requests
import re
from src import constants
from . import utils

class CmsScraper:
    """
    Simple webscraper that scrapes data from the CMS
    """
    def __init__(self, challenge_id):
        self.__session = requests.Session()
        self.__challenge_id = challenge_id
        self.__challenge_chlc = None
        self.__application_chlc = None
        self.__git_repo = None
        self.__scrape_cms()

    def get_challenge_chlc(self):
        return self.__challenge_chlc

    def get_application_chlc(self):
        return self.__application_chlc

    def get_git_repo(self):
        return self.__git_repo

    def validate_credentials(self):
        return True

    def __scrape_cms(self):
        '''
        Scrapes the cms to retrieve 
        '''
        # Get CSRF token for login
        csrf_token = self.__fetch_csrf_token()

        # Retrieve cookies from logging into the CMS
        cookies = self.__login_to_cms(csrf_token)

        # Scrape the challenge screen and return application endpoint
        application_endpoint = self.__scrape_challenge_screen(cookies)

        self.__scrape_application_screen(cookies, application_endpoint)

    def __fetch_csrf_token(self):
        """
        Get request to retrieve the CSRF token for logging in
        """
        # Get csrf token and cookies
        result = self.__session.get(constants.CMS_LOGIN_URL)

        print(result)

        # Check if result was successful
        if not result.ok:
            print('Scraper Error: fetching CSRF token failed')
            return None

        csrf_token = utils.parse_csrf_token(result)

        return csrf_token

    def __login_to_cms(self, csrf_token):
        """
        Login to the CMS using the CSRF token and return cookies for scraping
        """

        print(constants.CMS_EMAIL)
        print(constants.CMS_PASSWORD)

        # Create the login payload
        payload = {
            # '_username': constants.CMS_EMAIL,
            # '_password': constants.CMS_PASSWORD,
            '_username': 'ok',
            '_password': 'banana',
            '_csrf_token': csrf_token
        }

        # Login to CMS
        result = self.__session.post(
            constants.CMS_LOGIN_URL,
            data=payload,
        )

        print(result.status_code)

        # Check if login was successful
        if not result.ok:
            print('Scraper Error: logging into CMS failed')
            return None
        
        return result.cookies

    def __scrape_challenge_screen(self, cookies):
        """
        Get request to search for challenge id. Scrape challenge screen.
        Retrieve challenge CHLC and application screen endpoint.
        """
        # Query for CID
        result = self.__session.get(
            f'{constants.CMS_SEARCH_URL}?q={self.__challenge_id}',
            cookies=cookies
        )

        print('Scraping challenge screen')
        print(result)

        # Check if searching for challenge was successful
        if not result.ok:
            print('Scraper Error: scraping application page failed')
            return None

        # Initialize Challenge CHLC
        self.__challenge_chlc = utils.get_challenge_chlc(result)

        # Get application page url
        application_endpoint = utils.get_application_endpoint(result)

        return application_endpoint

    def __scrape_application_screen(self, cookies, application_endpoint):
        """
        Get request to retrieve application screen. Scrape the screen to
        retrieve application CHLC and github repository name.
        """
        # Query application page
        result = self.__session.get(
            f'{constants.CMS_URL}{application_endpoint}',
            cookies=cookies
        )

        print(result)

        # Check if requesting application page was successful
        if not result.ok:
            print('Scraper Error: scraping application page failed')
            return None

        # Initialize Application CHLC
        self.__application_chlc = utils.get_challenge_chlc(result)

        # Initialize Github repository name
        self.__git_repo = utils.get_git_repository(result)
