import requests
from bs4 import BeautifulSoup
import re
import csv


class ImmoWebScraper:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.data = {}
        self.id = self.extract_id()

    def extract_id(self):
        # Splitting the URL by slashes and taking the last element
        return self.url.rstrip('/').split('/')[-1]

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.content, "lxml")
        else:
            print(
                f"Failed to retrieve data, status code: {response.status_code}")

    def extract_property_type(self):
        element = self.soup.find('h1', class_='classified__title')
        if element:
            # Extracting the text
            text = element.get_text()

            # Using regular expression to replace all sequences of whitespace characters with a single space
            cleaned_text = re.sub(r'\s+', ' ', text).strip()

            # Assuming the property type is the first word before "for sale"
            property_type = cleaned_text.split(' for sale')[0]

            self.data['property_type'] = property_type
        else:
            self.data['property_type'] = None
            print("Property type element not found")

    def extract_price(self):
        # Use 'string' instead of 'text' to avoid DeprecationWarning
        elements = self.soup.find_all('span', string=re.compile(r'€\d+'))
        for element in elements:
            if '€' in element.string:  # Use .string to access the element's text
                price_text = element.string.strip()
                price_numeric = price_text.replace(
                    '€', '').replace(',', '').replace('.', '')
                try:
                    self.data['price'] = int(price_numeric)
                    return  # Exit the method after successfully finding the price
                except ValueError:
                    self.data['price'] = None
                    print(f"Could not convert price to int: '{price_text}'")
                    return  # Exit the method if conversion fails
        # Set price to None if no matching element is found
        self.data['price'] = None
        print("Price element not found")

    def extract_address_and_postcode(self):
        pass

    def extract_bedrooms(self):
        elements = self.soup.select(
            '#main-content > div:nth-child(3) > section > div > div > div > div:nth-child(1) > div:nth-child(1) > span, #main-content > div:nth-child(4) > section > div > div > div > div:nth-child(1) > div:nth-child(1) > span')
        # works for both houses and appartments

        if elements:
            text = elements[0].text.strip()
            self.data['bedrooms'] = self.extract_numeric(text)
        else:
            return None

    def extract_bathrooms(self):
        elements = self.soup.select(
            '#main-content > div:nth-child(3) > section > div > div > div > div:nth-child(1) > div:nth-child(2) > span,  #main-content > div:nth-child(4) > section > div > div > div > div:nth-child(1) > div:nth-child(2) > span, #accordion_b258cdb8-f587-42e7-b601-cd3053558d88 > table > tbody > tr:nth-child(9) > td')
        # works for both houses and appartments
        if elements:
            text = elements[0].text.strip()
            self.data['bathrooms'] = self.extract_numeric(text)
        else:
            return None

    def extract_living_area(self):
        elements = self.soup.select(
            '#main-content > div:nth-child(4) > section > div > div > div > div:nth-child(2) > div > span, #main-content > div:nth-child(3) > section > div > div > div > div:nth-child(2) > div:nth-child(1) > span')
        if elements:
            text = elements[0].text.strip()
            self.data['living_area'] = self.extract_numeric(text)
        else:
            return None

    def extract_floor(self):
        elements = self.soup.select(
            '#main-content > div:nth-child(4) > section > div > div > div > div:nth-child(3) > div:nth-child(2) > span, #main-content > div:nth-child(3) > section > div > div > div > div:nth-child(3) > div > span')
        if elements:
            text = elements[0].text.strip()
            self.data['floor'] = self.extract_numeric(text)
        else:
            return None

    def extract_energy_consumption(self):
        pass

    def extract_numeric(self, text):
        numbers = re.findall(r'\d+[\.,]?\d*', text)
        return '-'.join(numbers) if numbers else '0'

    def run(self):
        self.fetch_data()
        if self.soup:
            self.data['id'] = self.id  # Adding the ID to the data dictionary
            self.extract_property_type()
            self.extract_price()
            self.extract_address_and_postcode()
            self.extract_bedrooms()
            self.extract_bathrooms()
            self.extract_living_area()
            self.extract_floor()
            self.extract_energy_consumption()

        return self.data

    def save_to_csv(self, file_name):
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Writing the headers
            writer.writerow(self.data.keys())
            # Writing the data
            writer.writerow(self.data.values())


scraper = ImmoWebScraper(
    'https://www.immoweb.be/en/classified/house/for-sale/steenokkerzeel/1820/11151131')
result = scraper.run()
print(result)

# Save the result to a CSV file
scraper.save_to_csv('immoweb_data.csv')
