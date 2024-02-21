import json
from properties import ExtractPage
from FileUtils_class import FileUtils
from utils import Export
from pprint import pprint
import os
import os
from properties import ExtractPage
from FileUtils_class import FileUtils
from utils import Export
from pprint import pprint
import concurrent.futures

# Create an instance of the FileUtils class
fileUtils = FileUtils()

# Check if the directory exists
if not os.path.exists("data_scrapy"):
    # If not, create it
    os.makedirs("data_scrapy")
# Load the data from the file
data = FileUtils.read_json_file(r"data_scrapy\scrapy_output.json")

# Check for duplicates and update the file
duplicates_checked = FileUtils.return_solo_items(data=data)

print(len(duplicates_checked))

# Split duplicates_checked into the first 100 results
urls = duplicates_checked[:10]


def main(urls):
    dict_result = {}
    for url in urls:
        page = ExtractPage(url=url)
        result = page.to_dict()
        # print(result)

    # # Save dict_result into a CSV file
    FileUtils.write_dict_to_csv("result.csv", result)


if __name__ == "__main__":
    main(urls=urls)
