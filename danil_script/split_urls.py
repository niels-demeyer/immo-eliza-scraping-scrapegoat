import os
import json
from pprint import pprint
from urllib.parse import urlparse


# Reads a json file in
def read_json_file(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


file_path = "./scrapy_output.json"
scrapy_output = read_json_file(file_path=file_path)

# Takes the first 100 items
scrapy_output_100 = scrapy_output[:100]


# Returns the first 100 href
scrapy_output_100_href = [element['href'] for element in scrapy_output_100]

# List of all href
scrapy_output_href = [element['href'] for element in scrapy_output]

def split_url(url) -> dict:
    """
    Splits the given URL into its individual components and returns them as a dictionary.

    Args:
        url (str): The URL to be split.

    Returns:
        dict: A dictionary containing the individual components of the URL.

    Example:
        >>> url = "https://www.immoweb.be/en/classified/villa/for-sale/brasschaat/2930/11023593"
        >>> split_url(url)
        {
            "domain": "immoweb.be",
            "language": "en",
            "classified": True,
            "property_type": "villa",
            "type": "for-sale",
            "town_name": "brasschaat",
            "postal_code": "2930",
            "immoweb_code": "11023593"
        }
    """
    elements = url.split('/')
    elements = elements[1:]
    elements[1] = elements[1][4:]

    domain = elements[1]
    language = elements[2]
    classified = True if elements[3] == "classified" else False
    property_type = elements[4]
    type = elements[5]
    town_name = elements[6]
    postal_code = elements[7]
    immoweb_code = elements[8]
    split_dict = {
        "domain": domain, "language": language, "classified": classified,
        "property_type": property_type, "type": type, "town_name": town_name,
        "postal_code": postal_code, "immoweb_code": immoweb_code,
    }
    
    return split_dict



def combine_url(splitted_url: dict) -> str:
    """
    Combines the elements of a splitted URL dictionary into a single URL string.

    Args:
        splitted_url (dict): A dictionary containing the splitted URL elements.

    Returns:
        str: The combined URL string.

    """
    url = (
        f"https://www.{splitted_url['domain']}/"
        f"{splitted_url['language']}/"
        f"{'classified' if splitted_url['classified'] else 'not-classified'}/"
        f"{splitted_url['property_type']}/"
        f"{splitted_url['type']}/"
        f"{splitted_url['town_name']}/"
        f"{splitted_url['postal_code']}/"
        f"{splitted_url['immoweb_code']}"
    )
    return url


number_of_test = 1

for element in scrapy_output_href:
    url = element
    test_split = split_url(url)
    test_combine = combine_url(test_split)
    number_of_test += 1

    if test_combine != url:
        print(f"Something gone wrong with element #{number_of_test}.")
        print(test_split)
        print(test_combine)
        print(test_combine == url)
