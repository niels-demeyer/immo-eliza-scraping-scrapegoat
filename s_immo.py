import requests
from bs4 import BeautifulSoup
import re


url = 'https://www.immoweb.be/en/classified/new-real-estate-project-houses/for-sale/gent-mariakerke/9030/11146286'
data = requests.get(url)
print(url, data.status_code)
soup = BeautifulSoup(data.content, "lxml")
soup
my_data = []

# BEDROOMS
elements_bedrooms = soup.select(
    '#main-content > div:nth-child(3) > section > div > div > div > div:nth-child(1) > div:nth-child(1) > span, #main-content > div:nth-child(4) > section > div > div > div > div:nth-child(1) > div:nth-child(1) > span')
# works for both houses and appartments

if not elements_bedrooms:  # Check if the list is empty
    print("0")
else:
    for element in elements_bedrooms:
        # Extracting the text and stripping any leading/trailing whitespace from each matched element
        data_bedrooms = element.text.strip()
        print(data_bedrooms)

# BATHROOMS
elements_bathrooms = soup.select(
    '#main-content > div:nth-child(3) > section > div > div > div > div:nth-child(1) > div:nth-child(2) > span,  #main-content > div:nth-child(4) > section > div > div > div > div:nth-child(1) > div:nth-child(2) > span')
# works for both houses and appartments


if not elements_bathrooms:  # Check if the list is empty
    print("0")
else:
    for element in elements_bathrooms:
        # Extracting the text and stripping any leading/trailing whitespace from each matched element
        data_bathrooms = element.text.strip()
        print(data_bathrooms)

# LIVING AREA
elements_living_area = soup.select(
    '#main-content > div:nth-child(4) > section > div > div > div > div:nth-child(2) > div > span')
# works for both houses and appartments


if not elements_living_area:  # Check if the list is empty
    print("0")
else:

    for element in elements_living_area:
        # Extracting the text and stripping any leading/trailing whitespace from each matched element
        data_living_area = element.text.strip()

        # Using regular expression to find all numbers in the string
        numbers = re.findall(r'\d+[\.,]?\d*', data_living_area)

        # Joining the numbers back together, if needed, or just printing the first found number
        numeric_data = '-'.join(numbers) if numbers else '0'

        print(numeric_data)


#  #main-content > div:nth-child(4) > section > div > div > div > div:nth-child(2) > div > span
# #main-content > div:nth-child(4) > section > div > div > div > div:nth-child(2) > div > span
#  #main-content > div:nth-child(4) > section > div > div > div > div:nth-child(2) > div > span
