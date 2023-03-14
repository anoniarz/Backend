
import os
import requests
import re
import json
import collections as co
from bs4 import BeautifulSoup as bs


URL = f"https://www.ceneo.pl/133337315/opinie-2"
page = requests.get(URL)
doc = bs(page.text, "html.parser")

category = doc.find(class_="js_breadcrumbs breadcrumbs").find_all(
    class_="js_breadcrumbs__item breadcrumbs__item link")[-1].text.split()


print(" ".join(category))
