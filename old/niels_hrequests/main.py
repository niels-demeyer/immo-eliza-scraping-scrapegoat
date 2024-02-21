from properties import ExtractPage
from FileUtils_class import FileUtils
import os
import concurrent.futures
import pandas as pd
import glob

# Create an instance of the FileUtils class
fileUtils = FileUtils()


def process_url(url):
    page = ExtractPage(url=url)
    return page.to_dict()


def process_url_group(url_group):
    dict_result = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        dict_result = list(executor.map(process_url, url_group))
    return dict_result


def main(urls):
    # Split urls into chunks of 100
    url_chunks = [urls[i : i + 100] for i in range(0, len(urls), 100)]
    for i, url_chunk in enumerate(url_chunks):
        # Split each chunk into groups of 10
        url_groups = [url_chunk[j : j + 10] for j in range(0, len(url_chunk), 10)]
        for j, url_group in enumerate(url_groups):
            dict_result = process_url_group(url_group)
            # Save dict_result into a CSV file
            FileUtils.write_dict_to_csv(f"result_{i}_{j}.csv", dict_result)

    # Combine all CSV files into one and delete the individual files
    all_files = glob.glob("result_*.csv")
    df_from_each_file = (pd.read_csv(f, encoding="ISO-8859-1") for f in all_files)
    combined_df = pd.concat(df_from_each_file, ignore_index=True)
    combined_df.to_csv("output_requests.csv", index=False)
    for f in all_files:
        os.remove(f)


if __name__ == "__main__":
    # Check if the directory exists
    if not os.path.exists("data_scrapy"):
        # If not, create it
        os.makedirs("data_scrapy")
    # Load the data from the file
    data = FileUtils.read_json_file(
        r"data_scrapy\scrapy_output.json", encoding="ISO-8859-1"
    )
    # Split duplicates_checked into the first 100 results
    urls = [item["href"] for item in data]
    main(urls=urls)
