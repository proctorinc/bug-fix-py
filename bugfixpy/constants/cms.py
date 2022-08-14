"""
CMS Constants
"""


import keyring
from dotenv import load_dotenv

load_dotenv()

# CMS email
EMAIL = keyring.get_password("system", "CMS_EMAIL")

# CMS password
PASSWORD = keyring.get_password("system", "CMS_PASSWORD")

# URL for CMS
URL = "https://cms.securecodewarrior.com"

# URL to login to the CMS
LOGIN_URL = f"{URL}/login"

# URL to search for challenge in CMS
SEARCH_URL = f"{URL}/search"
