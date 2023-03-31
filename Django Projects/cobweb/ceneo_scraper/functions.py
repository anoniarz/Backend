from .models import Product
import re


def delete_from_db(ceneo_id):
    Product.objects.filter(product_id=ceneo_id).delete()


def link_to_id(adress):
    ceneo_id = "error: 1"
    try:
        ceneo_id = "".join((re.findall(r"\d{5,}", adress))[0])
    except:
        pass
    return ceneo_id


def try_or(f):
    try:
        return f
    except:
        return None
