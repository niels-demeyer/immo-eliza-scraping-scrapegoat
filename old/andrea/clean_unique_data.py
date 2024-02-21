import json

class Cleans_urls:
    """
    Takes a file with urls, extracts unique ids from it and outputs a json file with a page using it.
    """
    def __init__(self, file: str):
        # Loading unique_data json file into a dict
        self.raw_data = self.loads_file(source = file)

        # Getting unfiltered urls from the dict
        self.raw_urls = self.get_urls()
        # Counting them to see how many in total, just a nice to have for comparison
        self.numb_urls = len(self.raw_urls)  
        # Extracting the ids from the raw urls
        self.ids = set()
        for url in self.raw_urls:
            self.ids.add(self.extract_id(url))
        # Counting the unique ids, just a nice to have for comparison
        self.numb_ids= len (self.ids)
        # Builds a clean dictionary from the unique ids
        self.clean_urls_dict = self.builds_url()

    # Loads source file into json
    def loads_file (self, source: str) -> None:
        with open(source, "r") as f:
            return json.load(f)

    # Gets urls from json derived from source file
    def get_urls (self) -> list:
        return [x["href"] for x in self.raw_data]

    def extract_id(self, url):
        # Splitting the URL by slashes and returns the last element that is the ID
        return url.split('/')[-1]

    # Rebuilds URL with unique ID
    def builds_url (self):
        clean_urls = {}
        for id in self.ids:
            clean_urls[id] = "https://www.immoweb.be/en/classified/A/B/C/D/"+ str(id)
        return clean_urls
    # Exports to new json file
    def export_clean_urls_json (self, outfile):       
        
        with open(outfile, 'w', encoding='utf-8') as f:
            json.dump(self.clean_urls_dict, f, ensure_ascii=False, indent=4)
     
   
def main():  
    # File source and how many urls are going to be processed
    source = "unique_data.json"

    # Starts splitting
    test = Cleans_urls(file = source)
    # Exporting to file

    outfile = "clean_urls.json"
    test.export_clean_urls_json(outfile)


if __name__ == "__main__":
    main()