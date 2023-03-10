from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Review, Product
from datetime import datetime
from .forms import Url_f


from django.views.generic import DetailView
# Scraper
import requests
import re
import json
from bs4 import BeautifulSoup as bs


def link_to_id(adress):
    return "".join(re.findall(r"\d{5,}", adress))


def try_or(f):
    try:
        return f
    except:
        return None


def scrape(link):
    def try_or(f):
        try:
            return f
        except:
            return None

    flag = True
    n = 1
    local_id = 0
    ceneo_id = link_to_id(link)
    data = {f"{ceneo_id}": {}}
    while flag:
        URL = f"https://www.ceneo.pl/{ceneo_id}/opinie-{n}"
        page = requests.get(URL)
        doc = bs(page.text, "html.parser")
        content = doc.find_all(
            class_='user-post user-post__card js_product-review')

        product_name = try_or(doc.find(
            class_="product-top__product-info__name js_product-h1-link js_product-force-scroll js_searchInGoogleTooltip default-cursor").string)
        # Scraping
        for i in range(len(content)):
            local_id += 1
            review_id = try_or(content[i].get("data-entry-id"))
            author = try_or(content[i].find(
                class_="user-post__author-name").string[1:])
            # Recomendation
            try:
                if content[i].find(
                        class_="recommended").find("em").string == "Polecam":
                    is_recomended = True
                elif content[i].find(
                        class_="not-recommended").find("em").string == "Nie polecam":
                    is_recomended = False
                else:
                    is_recomended = None
            except:
                pass
            # No. stars
            stars = try_or(content[i].find(
                class_="user-post__score-count").string)
            # is_Verified
            try:
                is_verified = True if content[i].find(
                    class_="review-pz").find("em").string == "Opinia potwierdzona zakupem" else False
            except:
                is_verified = False
                pass
            # Date published
            date_p = try_or(content[i].find(
                class_="user-post__published").find_all("time")[0].get("datetime"))
            # Date Bought
            date_b = try_or(content[i].find(
                class_="user-post__published").find_all("time")[0].get("datetime"))
            # No. positive
            t_up = try_or(content[i].find(
                class_="vote-yes js_product-review-vote js_vote-yes").get("data-total-vote"))
            # No. negative
            t_down = try_or(content[i].find(
                class_="vote-no js_product-review-vote js_vote-no").get("data-total-vote"))
            # Opinion
            opinion = try_or(content[i].find(
                class_="user-post__text").text)
            # Features
            pos_features = []
            neg_features = []
            try:
                fea_list = content[i].find_all(
                    class_="review-feature__col")
                if fea_list[0].find(
                        class_="review-feature__title review-feature__title--positives").string == "Zalety":
                    pos_features.append(" ".join(x.string for x in fea_list[0].find_all(
                        class_="review-feature__item")))
                    neg_features.append(" ".join(x.string for x in fea_list[1].find_all(
                        class_="review-feature__item")))
                else:
                    neg_features.append(" ".join(x.string for x in fea_list[0].find_all(
                        class_="review-feature__item")))
            except:
                pass

            data[ceneo_id][review_id] = {
                "local_id": local_id,
                "product_id": ceneo_id,
                "product_name": product_name,
                "review_id": review_id,
                "author": author,
                "is_recomended": is_recomended,
                "is_verified": is_verified,
                "stars": stars,
                "date_p": date_p,
                "date_b": date_b,
                "t_up": t_up,
                "t_down": t_down,
                "opinion": opinion,
                "pos_features": pos_features,
                "neg_features": neg_features,
            }

        pagination = try_or(doc.find(class_="pagination"))
        try:
            if pagination.find(class_="pagination__item pagination__next") == None:
                flag = False
        except:
            flag = False
        n += 1

    with open(f'media\ceneo_reviews\{ceneo_id}.json', 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    if not Product.objects.filter(product_id=ceneo_id).exists():

        for ceneo_id, reviews in data.items():
            product_name = reviews[review_id].get('product_name')
            product = Product.objects.create(
                product_id=ceneo_id, product_name=product_name)

        for ceneo_id, reviews in data.items():
            for review_id, review in reviews.items():
                date_p = datetime.strptime(
                    review['date_p'], f'%Y-%m-%d %H:%M:%S')
                date_b = datetime.strptime(
                    review['date_b'], f'%Y-%m-%d %H:%M:%S')
                new_review = Review.objects.create(
                    product=product,
                    local_id=review['local_id'],
                    review_id=review['review_id'],
                    author=review['author'],
                    is_recomended=review['is_recomended'],
                    is_verified=review['is_verified'],
                    stars=review['stars'],
                    date_p=date_p,
                    date_b=date_b,
                    t_up=review['t_up'],
                    t_down=review['t_down'],
                    opinion=review['opinion'],
                    pos_features=review['pos_features'],
                    neg_features=review['neg_features'],
                )
                product.reviews.add(new_review)


# Adding Product
def add_product(request):
    if request.method == 'POST':
        form = Url_f(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url_f']
            scrape(url)
            return HttpResponseRedirect('/products')

    else:
        form = Url_f()
    return render(request, 'main/add_product.html', {'form': form})


def home(request):

    return render(request, 'main/home.html')


def about(request):

    return render(request, 'main/about.html')


def products(request):

    if request.method == 'POST':
        form = Url_f(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url_f']
            scrape(url)
    else:
        form = Url_f()

    context = {
        "products": Product.objects.all(),
        "reviews": Review.objects.all()
    }

    return render(request, 'main/products.html', context)


class ProductDetailView(DetailView):
    model = Product
    paginate_by = 2
