
import os
import requests
import re
import json
import collections as co
from bs4 import BeautifulSoup as bs


URL = f"https://www.ceneo.pl/133337315"
page = requests.get(URL)
doc = bs(page.text, "html.parser")

price = doc.find(class_="price-format nowrap").find(class_="value").string
price = re.sub(' ', '', price)

print(int(price))
