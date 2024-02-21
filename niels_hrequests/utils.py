import csv
from properties import Single



class Export (Single):
    """
    Class extracts a dictionary from a webpage with the property's characteristics.
    And contains methods to write those into a CSV line per line.
    Args:
        rawjson (json): raw json data from ExtractPage class
        link (str): link of a property to be scrapped
    """

    def __init__(self, rawjson, link: str) -> None: 
        
        self.page_dict = self.build_page_dict(rawjson= rawjson, link=link)

    def build_page_dict(self, rawjson, link: str) -> dict:
        """ Uses Single class to get each characteristc of the property.
            Returns a dictionary with all of them for the webpage
        """
        # Instantiate obj Single for the json data
        page_info = Single(rawjson)  
        # Initializates dictionary to be populated
        page_dict = {}

        # Calls all methods from Single to get the data for each key
        # TO BE FINISHED AFTER MERGE WITH DANIL
        # CAREFULL WITH KEEPING THE NAME OF THE KEY AS THE SAME AS csv_field_names IN MAIN (ADD IF MISSING)
        page_dict["Link"] = link
        page_dict["Price"] = page_info.get_price()
        page_dict["Kitchen"] = page_info.get_kitchen()
        page_dict["City"] = page_info.get_city()
        page_dict["Fireplace"] = page_info.get_fireplace()
        page_dict["Energy_sqm"] = page_info.get_energy_consumption()
        page_dict["Facades"] = page_info.get_facades()
        page_dict["Terrace_area"] = page_info.get_terrace_area()
        page_dict["Swimming_pool"] = page_info.get_swimming_pool()
        page_dict["State_building"] = page_info.get_state_of_building()
        page_dict["Construction_year"] = page_info.get_construction_year()        
        return page_dict
   
    def write_line_csv(self, filepath: str, field_names: list) -> None:
        """Takes a filepah, a dictionary (self.page_dict) and writes dictionary as a line into the CSV"""

        with open(filepath, 'a', newline='', encoding= 'utf-8') as csvfile:        
            writer = csv.DictWriter(csvfile, fieldnames = field_names)            
            writer.writerow(self.page_dict)

    @staticmethod
    def open_clean_csv(filepath:str, field_names: list) ->None:
        """
        Initializates a clean CSV file with a header
        """
        with open(filepath, 'w', newline='', encoding= 'utf-8') as csvfile:
            # Cleans CSV file if it was populated before
            csvfile.truncate()
            # Writes header
            writer = csv.DictWriter(csvfile, fieldnames = field_names)            
            writer.writeheader()
        
