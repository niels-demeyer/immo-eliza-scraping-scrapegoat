import os

from pprint import pprint

from FileUtils_class import FileUtils
from WebScraper_class import WebScraper

# Create an instance of the FileUtils class
fileUtils = FileUtils()

# Check if the directory exists
if not os.path.exists("data_playwright_niels"):
    # If not, create it
    os.makedirs("data_playwright_niels")

# Load the data from the file
data = FileUtils.read_json_file(r"data_playwright_niels\scrapy_output.json")

# Create a list of the urls that is 100 long
urls = [d["href"] for d in data[:1000]]

scraper = WebScraper(urls=urls)
scraper.scrape()
results = scraper.get_results()  # Add parentheses here
pprint(results)
