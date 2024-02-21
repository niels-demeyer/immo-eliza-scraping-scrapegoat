
from bs4 import BeautifulSoup
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class ImmoWebScraper:
    def __init__(self, url):
        self.url = url
        self.driver = None
        self.soup = None
        self.data = {}

    def fetch_data_with_selenium(self):
        # Setup Chrome with Selenium
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()))
        self.driver.get(self.url)

        # Wait for JavaScript to load
        # Adjust the time according to your needs
        self.driver.implicitly_wait(10)

        # Use BeautifulSoup to parse the page source
        self.soup = BeautifulSoup(self.driver.page_source, 'lxml')

        # Close the browser
        self.driver.quit()

    # Add your existing methods here, but call fetch_data_with_selenium instead of fetch_data


# Usage
scraper = ImmoWebScraper('your-target-url')
scraper.fetch_data_with_selenium()
# Call your data extraction methods here
