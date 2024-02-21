from bs4 import BeautifulSoup
import json
import requests
import pandas as pd


class ExtractPage:
    """
    Extracts a json from the page's html where we have all the characteristics of a property.
    Has a method to filter out which page has only one property or multiple listed inside.
    Args:
        url (str): url of a listing in the website.
    """

    def __init__(self, url: str) -> None:
        # Sets up request
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        }
        r = requests.get(url, headers=headers)
        content = r.content

        # Parses html getting into a script tag, cleans it and dumps as a json
        soup = BeautifulSoup(content, "html.parser")        
        raw_data = soup.find("script", attrs={"type":"text/javascript"}).text.replace("window.classified = ","" ).replace(";", "").strip()
        self.raw = (json.loads(raw_data))  

        # Tracks if page is a single property or a list of properties
        self.single = self.is_single_listing()   

        # Transforms it into a dataframe
        self.dataframe = pd.json_normalize(self.raw)
        self.keys = self.dataframe.keys()              

    def is_single_listing(self) -> bool: 
        # Uses key "cluster" to filter if multiple or single       
        if self.raw["cluster"] == "null" or self.raw["cluster"] is None:            
            return True
        else:
            return False

