import os
import json
from pprint import pprint


# Reads a json file in
def read_json_file(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


file_path = "./scrapy_output.json"
scrapy_output = read_json_file(file_path=file_path)

# Takes the first 100 items
scrapy_output_100 = scrapy_output[0:100]
# pprint(scrapy_output_100)
# print(len(scrapy_output_100))

# Returns the first 100 href
scrapy_output_100_href = [x["href"] for x in scrapy_output_100]
pprint(scrapy_output_100_href)
