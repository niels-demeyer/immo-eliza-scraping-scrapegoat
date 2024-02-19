
from bs4 import BeautifulSoup
import json
import requests

url = "https://www.immoweb.be/en/classified/apartment/for-sale/gavere/9890/11140881"
r = requests.get(url).text
soup = BeautifulSoup(r, "html.parser")
overview_tag = soup.overview__item
script_tag = overview_tag.find(
    'overview_itenm', string=lambda t: 'window.dataLayer' in t)


# The rest of your code remains the same
data_string = script_tag.string.split('window.dataLayer = ')[1].split(';')[0]
# print(data_string)
data_json = json.loads(data_string)
classified_info = data_json[0]['classified']
# print(json.dumps(data_json, indent=4))
print(classified_info)
