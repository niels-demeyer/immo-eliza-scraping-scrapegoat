from properties import ExtractPage
from FileUtils_class import FileUtils
import os
import pandas as pd
import glob

# Constants
CHUNK_SIZE = 100
GROUP_SIZE = 10
ENCODING = "ISO-8859-1"
DATA_DIR = "data_scrapy"
URLS_FILE = f"{DATA_DIR}/format_clean_urls3.json"
OUTPUT_FILE = "output_requests.csv"

# Create an instance of the FileUtils class
file_utils = FileUtils()


def main(urls, start, end, table_name):
    # Select a batch of URLs
    batch_urls = urls[start:end]
    url_chunks = ExtractPage.split_into_chunks(batch_urls, CHUNK_SIZE)
    for i, url_chunk in enumerate(url_chunks):
        url_groups = ExtractPage.split_into_chunks(url_chunk, GROUP_SIZE)
        for j, url_group in enumerate(url_groups):
            extract_page_objects = ExtractPage.process_url_group(url_group)
            results = [obj.to_dict() for obj in extract_page_objects]
            # Save results to SQLite database instead of CSV
            FileUtils.write_dict_to_sqlite("my_database.sqlite", table_name, results)


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    data = file_utils.read_json_file(URLS_FILE, encoding=ENCODING)
    urls = [item["href"] for item in data]
    # Process the first 500 URLs
    main(urls, start=0, end=500, table_name="first_500")
