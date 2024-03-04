import requests
from bs4 import BeautifulSoup

# Send a GET request to the website
url = "https://google.com"
response = requests.get(url)

# Create a BeautifulSoup object
soup = BeautifulSoup(response.text, "html.parser")

# Find and extract specific elements from the HTML
# For example, let's extract all the links on the page
links = soup.find_all("a")
for link in links:
    print(link.get("href"))