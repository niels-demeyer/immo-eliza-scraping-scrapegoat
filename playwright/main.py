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

# Split duplicates_checked into ten parts starting from index 99
urls = [duplicates_checked[i * 10 + 99 : (i + 1) * 10 + 99] for i in range(10)]


def scrape_urls(urls):
    scraper = WebScraper(urls=urls)
    scraper.scrape()
    return scraper.get_results()


# Use ThreadPoolExecutor to scrape each part concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(scrape_urls, urls)

# After the results are obtained
for result in results:
    pprint(result)
    FileUtils.write_dict_to_csv("results.csv", result)
