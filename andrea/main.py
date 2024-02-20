import json
from properties import ExtractPage
from utils import Export






links = ['https://www.immoweb.be/en/classified/apartment/for-sale/etterbeek/1040/11153755',
        'https://www.immoweb.be/en/classified/apartment/for-sale/evere/1140/11012764',
        'https://www.immoweb.be/en/classified/house/for-sale/anderlecht/1070/11150049',
        'https://www.immoweb.be/en/classified/house/for-sale/woluwe-saint-pierre/1150/11153143',
        'https://www.immoweb.be/en/classified/flat-studio/for-sale/ixelles/1050/11153142',
        'https://www.immoweb.be/en/classified/apartment/for-sale/gavere/9890/11140887',
        'https://www.immoweb.be/en/classified/apartment/for-sale/ixelles/1050/11153221',
        'https://www.immoweb.be/en/classified/apartment/for-sale/grivegnee/4030/11151417',
        'https://www.immoweb.be/en/classified/apartment/for-sale/brussels-city/1000/11152299',
        'https://www.immoweb.be/en/classified/apartment/for-sale/blankenberge/8370/11135884',
        'https://www.immoweb.be/en/classified/house/for-sale/steenokkerzeel/1820/11151131',
        'https://www.immoweb.be/en/classified/apartment/for-sale/brasschaat/2930/11152796',
        'https://www.immoweb.be/en/classified/apartment/for-sale/knokke/8300/11150926',
        'https://www.immoweb.be/en/classified/apartment/for-sale/woluwe-saint-lambert/1200/11146192',
        'https://www.immoweb.be/en/classified/flat-studio/for-sale/waregem/8790/11020971',
        'https://www.immoweb.be/en/classified/flat-studio/for-sale/waregem/8790/10971611',
        'https://www.immoweb.be/en/classified/apartment/for-sale/molenbeek-saint-jean/1080/11149338',
        'https://www.immoweb.be/en/classified/apartment/for-sale/bruxelles/1000/11148735',
        'https://www.immoweb.be/en/classified/apartment/for-sale/lier/2500/11047983',
        'https://www.immoweb.be/en/classified/apartment/for-sale/namur/5000/10907913',
        'https://www.immoweb.be/en/classified/flat-studio/for-sale/knokke/8300/11108596',
        'https://www.immoweb.be/en/classified/apartment/for-sale/fayt-lez-manage/7170/10682127',
        'https://www.immoweb.be/en/classified/exceptional-property/for-sale/braives/4260/11146418',
        'https://www.immoweb.be/en/classified/apartment/for-sale/maisieres/7020/10990864',
        'https://www.immoweb.be/en/classified/service-flat/for-sale/asse/1730/11100778']

def main():
    
    
    csv_field_names = ["Link", "Price", "Kitchen", "City", "Fireplace", "Energy_sqm","Facades", "Terrace_area", "Swimming_pool","State_building", "Construction_year"]
    csv_filepath = "listing.csv"
    
    Export.open_clean_csv(filepath = csv_filepath , field_names = csv_field_names)



    # Looping links
    for link in links:
        # Initializes extraction of html and parsing
        extract = ExtractPage(link)

        # Filters if page has only one property of many listed inside
        if extract.single:
            page = Export(rawjson= extract.raw, link = link )
            page.write_line_csv(filepath = csv_filepath , field_names = csv_field_names)

        else:
            pass


if __name__ == "__main__":
    main()




"""
# Handy json dump to catch errors
url_question = "https://www.immoweb.be/en/classified/apartment/for-sale/fayt-lez-manage/7170/10682127"
question = ExtractPage(url_question)
namefile = "testing.json"
with open(namefile, 'w', encoding='utf-8') as f:
    json.dump(question.raw, f, ensure_ascii=False, indent=4)
"""
