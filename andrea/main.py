from properties import ExtractPage, Single, Multiple

def main():
    # testing link with multiple listings inside
    url = "https://www.immoweb.be/en/classified/new-real-estate-project-apartments/for-sale/seraing/4100/11109402"

    # testing link with single listing on page
    #url = "https://www.immoweb.be/en/classified/apartment/for-sale/berchem-sainte-agathe/1082/11024799"

    # Initializes extraction of html and parsing
    extract = ExtractPage(url)

    # Filters if page has only one property of many listed inside
    if extract.single:
        test = Single (extract.raw)
        # For now just printing all the properties that where extracted
        # Later to put it into a dictionary or other data type to write on the csv
        print (f"Id is {test.get_id()}")
        print (f"Price is {test.get_price()}")
        print (f"The property type is {test.get_type()}")
        print (f"The property subtype is {test.get_subtype()}")
        print (f"Has kitchen? {test.get_kitchen()}")
        print (f"City is {test.get_city()}")
        print (f"The number of bedroomns is {test.get_number_bedrooms()}")
        print (f"The number of bathrooms is {test.get_number_bathrooms()}")
        print (f"The living area is {test.get_living_area()}")
        print (f"Has a fireplace? {test.get_fireplace()}")
        print( f"Energy consumption per sm is {test.get_energy_consumption()}")
        print (f"The number of facades is {test.get_facades()}")


    # If page has multiple properties listed inside
    else:
        print ("multiple")        
        test2 = Multiple(extract.raw)
        print(test2.number_unsold_unities)
        print(test2.unities)
        


if __name__ == "__main__":
    main()



"""
# Handy json dump to check stuff
namefile = "sample_single_listing.json"
with open(namefile, 'w', encoding='utf-8') as f:
    json.dump(test.data, f, ensure_ascii=False, indent=4)
"""