import requests
from bs4 import BeautifulSoup


url = 'https://www.immoweb.be/en/classified/new-real-estate-project-houses/for-sale/gent-gentbrugge/9050/11150513'
data = requests.get(url)
print(url, data.status_code)
soup = BeautifulSoup(data.content, "lxml")
soup
my_data = []

elements_bedrooms = soup.select(
    '#main-content > div:nth-child(3) > section > div > div > div > div:nth-child(1) > div:nth-child(1) > span, #main-content > div:nth-child(4) > section > div > div > div > div:nth-child(1) > div:nth-child(1) > span')
# works for both houses and appartments

for element in elements_bedrooms:
    # Extracting the text and stripping any leading/trailing whitespace from each matched element
    data_bedrooms = element.text.strip()
    print(data_bedrooms)

elements_bathrooms = soup.select(
    '#main-content > div:nth-child(3) > section > div > div > div > div:nth-child(1) > div:nth-child(2) > span,  #main-content > div:nth-child(4) > section > div > div > div > div:nth-child(1) > div:nth-child(2) > span')
# works for both houses and appartments

for element in elements_bathrooms:
    # Extracting the text and stripping any leading/trailing whitespace from each matched element
    data_bathrooms = element.text.strip()
    print(data_bathrooms)

# main-content > div:nth-child(3) > section > div > div > div > div:nth-child(1) > div:nth-child(2) > span
# #main-content > div:nth-child(4) > section > div > div > div > div:nth-child(1) > div:nth-child(2) > span
