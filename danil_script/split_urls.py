import os
import json
from pprint import pprint


# Reads a json file in
def read_json_file(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


file_path = "./scrapy_output.json"
scrapy_output = read_json_file(file_path=file_path)

print(scrapy_output)

# Takes the first 100 items
# scrapy_output_100 =

# Returns the first 100 href (use the scrapy_output_100 variable)
scrapy_output_100_href = []


# Define a function that splits the hrefs correctly, make sure it returns a dictionary in the following way
# Input:
# https://www.immoweb.be/en/classified/villa/for-sale/brasschaat/2930/11023593
# Output:
# {"domain": "immoweb.be", "language": "en", "classified": true, "type": "for-sale": true, "town_name": "brasschaat", "postal_code": 2930, "immoweb_code": 11023593}


# Input:
# {"domain": "immoweb.be", "language": "en", "classified": true, "type": "for-sale": true, "town_name": "brasschaat", "postal_code": 2930, "immoweb_code": 11023593}
# Output:
# https://www.immoweb.be/en/classified/villa/for-sale/brasschaat/2930/11023593
# Define a function that puts the href back together