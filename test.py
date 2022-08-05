import requests
from bs4 import BeautifulSoup

session = requests.Session()
result = requests.Session().get("https://google.com")
soup = BeautifulSoup(result.content, "html.parser")

print(type(soup))
