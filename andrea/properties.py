from bs4 import BeautifulSoup
import json
import requests

class ExtractPage:
    """
        Extracts a json from the page's html where we have all the characteristics of a property.
        Has a method to filter out which page has only one property or multiple listed inside.
        Args:
            url (str): url of a listing in the website.
    """
    def __init__(self, url: str) -> None: 
        # Sets up request
        headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
        r = requests.get(url, headers = headers)
        content = r.content

        # Parses html getting into a script tag, cleans it and dumps as a json
        soup = BeautifulSoup(content, "html.parser")        
        raw_data = soup.find("script", attrs={"type":"text/javascript"}).text.replace("window.classified = ","" ).replace(";", "").strip()
        self.raw = (json.loads(raw_data))  
        # Tracks if page is a single property or a list of properties
        self.single = self.is_single_listing()                

    def is_single_listing(self) -> bool: 
        # Uses key "cluster" to filter if multiple or single       
        if self.raw["cluster"] == "null" or self.raw["cluster"] == None:            
            return True
        else:
            return False


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
            energy_sm = self.data["transaction"]["certificates"]["primaryEnergyConsumptionPerSqm"]
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
            swimming_pool = self.data['property']['hasSwimmingPool']
            if swimming_pool:
                return 1
            else:
                return 0
        except Exception as e:
            return str(e)

    def get_state_of_building(self):
        try:
            state_of_building = self.data['property']['building']['condition']
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
            construction_year = self.data['property']['building']['constructionYear']
            if construction_year:
                return construction_year
            else:
                return None
        except Exception as e:
            return str(e)
        
    