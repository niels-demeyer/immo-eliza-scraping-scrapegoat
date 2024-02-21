from properties import ExtractPage
from FileUtils_class import FileUtils
import os

# Create an instance of the FileUtils class
fileUtils = FileUtils()

# Check if the directory exists
if not os.path.exists("data_scrapy"):
    # If not, create it
    os.makedirs("data_scrapy")
# Load the data from the file
data = FileUtils.read_json_file(r"data_scrapy\scrapy_output.json")


# Split duplicates_checked into the first 100 results
urls = [item["href"] for item in data[:100]]

# print(urls)


def main(urls):
    dict_result = []
    for url in urls:
        page = ExtractPage(url=url)
        result = page.to_dict()
        dict_result.append(result)

    # print(dict_result[0])
    # # Save dict_result into a CSV file
    FileUtils.write_dict_to_csv("result.csv", dict_result)


if __name__ == "__main__":
    main(urls=urls)
