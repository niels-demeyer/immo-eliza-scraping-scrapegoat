import csv
from properties import Single



class Export (Single):

    def __init__(self, rawjson, link):   
     
        self.page_dict = self.build_page_dict(rawjson= rawjson, link=link)

    def build_page_dict(self, rawjson, link) -> dict:
        page_info = Single(rawjson)  

        page_dict = {}
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
   
    def write_line_csv(self,filepath, field_names) -> None:
        """Takes a filepah, a dictionary and exports them into a csv file"""

        with open(filepath, 'a', newline='', encoding= 'utf-8') as csvfile:        
            writer = csv.DictWriter(csvfile, fieldnames = field_names)            
            writer.writerow(self.page_dict)

    @staticmethod
    def open_clean_csv(filepath, field_names):
        with open(filepath, 'w', newline='', encoding= 'utf-8') as csvfile:
            csvfile.truncate()
            writer = csv.DictWriter(csvfile, fieldnames = field_names)            
            writer.writeheader()
        
