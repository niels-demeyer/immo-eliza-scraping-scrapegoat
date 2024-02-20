import os
import concurrent.futures

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


# Check for duplicates and update the file
duplicates_checked = FileUtils.return_solo_items(data=data)

print(len(duplicates_checked))

# Split duplicates_checked into four parts
urls1 = duplicates_checked[:25]
urls2 = duplicates_checked[25:50]
urls3 = duplicates_checked[50:75]
urls4 = duplicates_checked[75:100]


def scrape_urls(urls):
    scraper = WebScraper(urls=urls)
    scraper.scrape()
    return scraper.get_results()


# Use ThreadPoolExecutor to scrape each part concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    results1, results2, results3, results4 = executor.map(
        scrape_urls, [urls1, urls2, urls3, urls4]
    )

pprint(results1)
pprint(results2)
pprint(results3)
pprint(results4)
