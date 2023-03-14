
import os
import requests
import re
import json
import collections as co
from bs4 import BeautifulSoup as bs


URL = f"https://www.ceneo.pl/98430083/opinie-2"
page = requests.get(URL)
doc = bs(page.text, "html.parser")

price = doc.find(class_="price-format nowrap").find(class_="value").string


print(price)
