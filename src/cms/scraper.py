from bs4 import BeautifulSoup
import requests
import re
from constants import (
    CMS_EMAIL,
    CMS_PASSWORD,
    CMS_URL,
    CMS_LOGIN_URL,
    CMS_SEARCH_URL
)

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
        result = self.__session.get(CMS_LOGIN_URL)

        # Check if result was successful
        if not result.ok:
            print('Scraper Error: fetching CSRF token failed')
            return None

        # Parse CSRF token
        soup = BeautifulSoup(result.content, 'html.parser')
        csrf_token = soup.find('input', {'name': '_csrf_token'}).get('value')

        return csrf_token

    def __login_to_cms(self, csrf_token):
        """
        Login to the CMS using the CSRF token and return cookies for scraping
        """
        # Create the login payload
        payload = {
            '_username': CMS_EMAIL,
            '_password': CMS_PASSWORD,
            '_csrf_token': csrf_token
        }

        # Login to CMS
        login_result = self.__session.post(
            CMS_LOGIN_URL,
            data=payload,
        )

        # Check if login was successful
        if not login_result.ok:
            print('Scraper Error: logging into CMS failed')
            return None
        
        return login_result.cookies

    def __scrape_challenge_screen(self, cookies):
        """
        Get request to search for challenge id. Scrape challenge screen.
        Retrieve challenge CHLC and application screen endpoint.
        """
        # Query for CID
        result = self.__session.get(
            f'{CMS_SEARCH_URL}?q={self.__challenge_id}',
            cookies=cookies
        )

        # Check if searching for challenge was successful
        if not result.ok:
            print('Scraper Error: scraping application page failed')
            return None

        # Get page text + beautify
        soup = BeautifulSoup(result.content, 'html.parser') #, parse_only=SoupStrainer('a', href=True))

        # Initialize Challenge CHLC
        self.__challenge_chlc = self.__get_challenge_chlc(soup)

        # Get application page url
        application_endpoint = self.__get_application_endpoint(soup)

        return application_endpoint

    def __scrape_application_screen(self, cookies, application_endpoint):
        """
        Get request to retrieve application screen. Scrape the screen to
        retrieve application CHLC and github repository name.
        """
        # Query application page
        result = self.__session.get(
            f'{CMS_URL}{application_endpoint}',
            cookies=cookies
        )

        # Check if requesting application page was successful
        if not result.ok:
            print('Scraper Error: scraping application page failed')
            return None
            
        # Get page text + beautify
        soup = BeautifulSoup(result.content, 'html.parser')

        # Initialize Application CHLC
        self.__application_chlc = self.__get_challenge_chlc(soup)

        # Initialize Github repository name
        self.__git_repo = self.__get_git_repository(soup)

    def __get_challenge_chlc(self, soup):
        """
        Get the value of the challenge CHLC that is located in a link
        that contains SCW's base Jira url
        """
        JIRA_URL = 'https://securecodewarrior.atlassian.net/browse/'
        return self.__get_value_from_link(soup, JIRA_URL)

    def __get_git_repository(self, soup):
        """
        Get the value of the Github repository that is located in a link
        that contains SCW's base Github url
        """
        GIT_URL = 'https://github.com/SCWContent/'
        return self.__get_value_from_link(soup, GIT_URL)

    def __get_value_from_link(self, soup, url_pattern):
        """
        Searches all links on page and returns the value after the url pattern in the href
        """
        links = soup.findAll('a', href=True)

        for link in links:
            href = link['href']
            if (url_pattern in href):
                return href.split(url_pattern)[1]

    def __get_application_endpoint(self, soup):
        """
        Searches all links on the page for the applications/id/show url 
        """
        links = soup.findAll('a', href=True)
        for link in links:
            href = link['href']
            if re.search('/show$', href):
                return href