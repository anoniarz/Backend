import requests
from bs4 import BeautifulSoup as bs


URL = f"https://www.ceneo.pl/94823130/opinie-2"
page = requests.get(URL)
doc = bs(page.text, "html.parser")
pages = doc.find_all(
    class_="user-post user-post__card js_product-review").string


with open("test.html", "w") as f:
    f.write(pages[0])
