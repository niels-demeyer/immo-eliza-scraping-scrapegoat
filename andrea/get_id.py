import json


class Getid:
    """
    Takes a file with urls and returns a set with the unique IDs extracted from the URLs via self.ids.
    """
    def __init__(self, file, numb_tests):
       
        self.file = file 
        self.raw_data = self.loads_file()
        self.raw_urls = self.get_urls(numb_tests)       
        self.ids = set()
        for url in self.raw_urls:
            self.ids.add(self.extract_id(url))

    
    def loads_file (self):
        with open(self.file, "r") as f:
            return json.load(f)

    def get_urls (self, number):
        return [x["href"] for x in self.raw_data[0:number]]

    def extract_id(self, url):
        # Splitting the URL by slashes and taking the last element
        return url.split('/')[-1]
        
# File source and how many urls are going to be processed
source = "scrapy_output.json"
numb_tests = 100

# Starts splitting
test = Getid(file = source, numb_tests= numb_tests)
# Prints set with unique ids
print (test.ids)
