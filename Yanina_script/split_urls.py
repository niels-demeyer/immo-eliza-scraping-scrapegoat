import os
import json
from pprint import pprint


# Reads a json file in
def read_json_file(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


file_path = "./Yanina_script/scrapy_output.json"
scrapy_output = read_json_file(file_path)

# Takes the first 100 items
scrapy_output_100 = scrapy_output[0:100]
# pprint(scrapy_output_100)
# print(len(scrapy_output_100))

# Returns the first 100 href
scrapy_output_100_href = [x["href"] for x in scrapy_output_100]
print(scrapy_output_100_href)


# Define a function that splits the hrefs correctly, make sure it returns a dictionary in the following way
# Input:
# https://www.immoweb.be/en/classified/villa/for-sale/brasschaat/2930/11023593
# Output:
# {"domain": "immoweb.be", "language": "en", "classified": true, "type": "for-sale": true, "town_name": "brasschaat", "postal_code": 2930, "immoweb_code": 11023593}


def split_hrefs(url):
    # Remove the protocol (http:// or https://) and split the URL
    parts = url.replace(
        "http://www.", "").replace("https://www.", "").split('/')

    # Extract the domain name
    domain = parts[0]

    # Initialize the dictionary with default values
    result = {
        "domain": domain,
        "language": None,
        "classified": False,
        "property_type": None,
        "type": None,  # for-sale by default
        "town_name": None,
        "postal_code": None,
        "immoweb_code": None
    }

    result['language'] = parts[1]

    # Set 'classified' to True if 'classified' is in the URL parts
    result['classified'] = "classified" in parts

    result["property_type"] = parts[3]

    result['type'] = parts[4]

    if len(parts) > 5:
        result['town_name'] = parts[5]
        try:
            result['postal_code'] = int(parts[6])
        except ValueError:
            result['postal_code'] = None

    result['immoweb_code'] = int(parts[-1])

    return result


processed_hrefs = [split_hrefs(href) for href in scrapy_output_100_href]
print(processed_hrefs)

# Input:
# {"domain": "immoweb.be", "language": "en", "classified": true, "type": "for-sale": true, "town_name": "brasschaat", "postal_code": 2930, "immoweb_code": 11023593}
# Output:
# https://www.immoweb.be/en/classified/villa/for-sale/brasschaat/2930/11023593
# Define a function that puts the href back together


def merge_values_to_href(data):
    # Start with the protocol and domain
    url = f"https://www.{data['domain']}"

    # Add the language part
    if data.get('language'):
        url += f"/{data['language']}"

    # Add the 'classified' part if it's True
    if data.get('classified'):
        url += "/classified"

    # Add the property type part
    if data.get('property_type'):
        property_type = data.get("property_type")
        url += f"/{property_type}"

    # Add the type part (for-sale...)
    type_part = "for-sale" if data.get(
        'type') == "for sale" else "for-rent"
    url += f"/{type_part}"

    # Add the town name and postal code
    if data.get('town_name') and data.get('postal_code'):
        url += f"/{data['town_name']}/{data['postal_code']}"

    # Add the immoweb code
    if data.get('immoweb_code'):
        url += f"/{data['immoweb_code']}"

    return url


property_url = [merge_values_to_href(info) for info in processed_hrefs]
print(property_url)
