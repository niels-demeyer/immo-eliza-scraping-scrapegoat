import json


class Getid:
    """
    Takes a file with urls and returns a set with the unique IDs extracted from the URLs via self.ids.
    """
    def __init__(self, file):
       
        self.file = file 
        self.raw_data = self.loads_file()
        self.raw_urls = self.get_urls()
        self.numb_urls = len(self.raw_urls)       
        self.ids = set()
        for url in self.raw_urls:
            self.ids.add(self.extract_id(url))
        self.numb_ids= len (self.ids)
    
    # Loads json
    def loads_file (self):
        with open(self.file, "r") as f:
            return json.load(f)

    def get_urls (self):
        return [x["href"] for x in self.raw_data]

    def extract_id(self, url):
        # Splitting the URL by slashes and taking the last element
        return url.split('/')[-1]
        
# File source and how many urls are going to be processed
source = "scrapy_output.json"


# Starts splitting
test = Getid(file = source)
# Prints set with unique ids
print (test.ids)
print (test.numb_urls)
print(test.numb_ids)
