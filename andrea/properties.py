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
        return self.data["transaction"]["sale"]["price"]

    def get_postal_code(self):
        return self.data["property"]["location"]["postalCode"]

    def get_city(self):
        return self.data["property"]["location"]["locality"]

    def get_kitchen(self):
        if self.data["property"]["kitchen"]["type"] != "NOT_INSTALLED":
            return 1
        else:
            return 0

    def get_fireplace(self):
        if self.data["property"]["fireplaceExists"]:
            return 1
        else:
            return 0

    def get_facades(self):
        facade = self.data["property"]["building"]["facadeCount"]
        if facade != "null" or facade != None:
            return facade
        else:
            return None
    
    def get_energy_consumption(self):
        energy_sm = self.data["transaction"]["certificates"]["primaryEnergyConsumptionPerSqm"]
        if energy_sm != "null" or energy_sm != None:
            return energy_sm
        else:
            return None
    # So far in my tests I can get any characteristcs, keys are listed in the googlesheets tab Json

# WORKING ON IT
# if will probably inherit from Single for some properties (DO TO) 
class Multiple:
    def __init__(self, raw):
        self.data = raw 
        self.number_unities = self.count_unities()
        self.unities = []

        # each unity has an id, subtype, price, bedroom, surface
        # I am thinking about what is the best datatype for this
        # but I am thinking about making a list of lists

    def count_unities(self):
        # not finished in test
        print(self.data["cluster"]["units"][0]["items"])
        pass
    def get_unities_properties(self):
        pass   



