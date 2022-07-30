from bs4 import BeautifulSoup
from src import constants

def get_soup(result):
    # Get page text + beautify
    soup = BeautifulSoup(result.content, 'html.parser')

    return soup

def get_challenge_chlc(result):
    """
    Get the value of the challenge CHLC that is located in a link
    that contains SCW's base Jira url
    """
    soup = get_soup(result)
    return self.__get_value_from_link(soup, constants.JIRA_URL)

def get_git_repository(result):
    """
    Get the value of the Github repository that is located in a link
    that contains SCW's base Github url
    """
    soup = get_soup(result)
    return self.__get_value_from_link(soup, constants.GIT_URL)

def get_value_from_link(result, url_pattern):
    """
    Searches all links on page and returns the value after the url pattern in the href
    """
    soup = get_soup(result)
    links = soup.findAll('a', href=True)

    for link in links:
        href = link['href']
        if (url_pattern in href):
            return href.split(url_pattern)[1]

def get_application_endpoint(result):
    """
    Searches all links on the page for the applications/id/show url 
    """
    soup = get_soup(result)
    links = soup.findAll('a', href=True)
    for link in links:
        href = link['href']
        if re.search('/show$', href):
            return href

def parse_csrf_token(result):
    """
    Parses CSRF token from CMS login page using beautiful soup
    """
    soup = BeautifulSoup(result.content, 'html.parser')
    csrf_token = soup.find('input', {'name': '_csrf_token'}).get('value')
    
    return csrf_token
