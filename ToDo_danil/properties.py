import hrequests
from bs4 import BeautifulSoup
import json
from selectolax.parser import HTMLParser


class ExtractPage:
    """
    Extracts a json from the page's html where we have all the characteristics of a property.
    Has a method to filter out which page has only one property or multiple listed inside.
    Args:
        url (str): url of a listing in the website.
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        }
        try:
            self.raw = self.get_raw_data()
            self.single = self.is_single_listing()
        except ValueError:
            print(f"Error: No script tag found in the HTML for URL {self.url}")
            self.raw = None
            self.single = None

    def get_raw_data(self):
        response = self.make_request()
        if response is not None:
            content = response.content
            html = HTMLParser(content)
            raw_data = self.extract_data_from_script(html)
            if raw_data is not None:
                return json.loads(raw_data)
            else:
                raise ValueError("No script tag found in the HTML.")
        else:
            return None

    def make_request(self):
        while True:
            try:
                return hrequests.get(self.url, headers=self.headers)
            except hrequests.exceptions.ClientException as e:
                print(f"An error occurred while making a request to {self.url}: {e}")
                pass


    def extract_data_from_script(self, html):
        script = html.css_first("script[type='text/javascript']")
        if script:
            return (
                script.text()
                .replace("window.classified = ", "")
                .replace(";", "")
                .strip()
            )
        else:
            print("No script tag found in the HTML.")
            return None

    def is_single_listing(self) -> bool:
        # Uses key "cluster" to filter if multiple or single
        return self.raw and (
            self.raw["cluster"] == "null" or self.raw["cluster"] is None
        )

    def to_dict(self):
        return {
            "url": self.url,
            "raw": self.raw,
            "single": self.single,
        }


class Single:
    """
    Extracts characteristics of a page that has only one property listed inside.
    Arg:
    raw (json): Json file extracted via the class ExtractPage.

    """

    def __init__(self, raw):
        self.data = raw

    def get_price(self):
        try:
            return self.data["transaction"]["sale"]["price"]
        except Exception as e:
            return str(e)

    def get_postal_code(self):
        try:
            return self.data["property"]["location"]["postalCode"]
        except Exception as e:
            return str(e)

    def get_city(self):
        try:
            return self.data["property"]["location"]["locality"]
        except Exception as e:
            return str(e)

    def get_kitchen(self):
        try:
            if self.data["property"]["kitchen"]["type"] != "NOT_INSTALLED":
                return 1
            else:
                return 0
        except Exception as e:
            return str(e)

    def get_fireplace(self):
        try:
            if self.data["property"]["fireplaceExists"]:
                return 1
            else:
                return 0
        except Exception as e:
            return str(e)

    def get_facades(self):
        try:
            facade = self.data["property"]["building"]["facadeCount"]
            if facade != "null" and facade != None:
                return facade
            else:
                return None
        except Exception as e:
            return str(e)

    def get_energy_consumption(self):
        try:
            energy_sm = self.data["transaction"]["certificates"][
                "primaryEnergyConsumptionPerSqm"
            ]
            if energy_sm != "null" or energy_sm != None:
                return energy_sm
            else:
                return None
        except Exception as e:
            return str(e)

    def get_terrace_area(self):
        try:
            terrace_area = self.data["property"]["terraceSurface"]
            if terrace_area:
                return terrace_area
            else:
                return None
        except Exception as e:
            return str(e)

    def get_swimming_pool(self):
        try:
            swimming_pool = self.data["property"]["hasSwimmingPool"]
            if swimming_pool:
                return 1
            else:
                return 0
        except Exception as e:
            return str(e)

    def get_state_of_building(self):
        try:
            state_of_building = self.data["property"]["building"]["condition"]
            if state_of_building == "GOOD":
                return "good"
            elif state_of_building == "JUST_RENOVATED":
                return "just renovated"
            elif state_of_building == "AS_NEW":
                return "as new"
            elif state_of_building == "TO_BE_DONE_UP":
                return "to be done up"
            elif state_of_building == "TO_RENOVATE":
                return "to renovate"
            else:
                return state_of_building
        except Exception as e:
            return str(e)

    def get_construction_year(self):
        try:
            construction_year = self.data["property"]["building"]["constructionYear"]
            if construction_year:
                return construction_year
            else:
                return None
        except Exception as e:
            return str(e)
