from properties import ExtractPage, Single, Multiple

def main():
    # testing now a link with multiple listings inside
    url = "https://www.immoweb.be/en/classified/new-real-estate-project-apartments/for-sale/seraing/4100/11109402"


    # Initializes extraction of html and parsing
    extract = ExtractPage(url)

    # Filters if page has only one property of many listed inside
    if extract.single:
        test = Single (extract.raw)
        # For now just printing all the properties that where extracted
        # Later to put it into a dictionary or other data type to write on the csv
        print (f"Price is {test.get_price()}")
        print (f"Has kitchen? {test.get_kitchen()}")
        print (f"City is {test.get_city()}")
        print (f"Has a fireplace? {test.get_fireplace()}")
        print( f"Energy consumption per sm is {test.get_energy_consumption()}")
        print (f"The number of facades is {test.get_facades()}")
    # If page has multiple properties listed inside
    else:
        print ("multiple")
        tes2 = Multiple(extract.raw)


if __name__ == "__main__":
    main()



"""
# Handy json dump to check stuff
namefile = "sample_single_listing.json"
with open(namefile, 'w', encoding='utf-8') as f:
    json.dump(test.data, f, ensure_ascii=False, indent=4)
"""