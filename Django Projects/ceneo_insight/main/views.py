from django.shortcuts import render
from .models import Reviews
from datetime import datetime
import requests, re
from bs4 import BeautifulSoup as bs
from .forms import Url_f
def link_to_id(adress):
    return "".join(re.findall(r"\d+{5,}", adress))

def scrape(link):
    def try_or(f):
        try:
            return f
        except:
            return None
    data = {}
    flag = True
    n = 1
    l_id = 0
    ceneo_id = link_to_id(link)
    print(ceneo_id)
    while flag:
        URL = f"https://www.ceneo.pl/{ceneo_id}/opinie-{n}"
        page = requests.get(URL)
        doc = bs(page.text, "html.parser")
        content = doc.find_all(
            class_='user-post user-post__card js_product-review')
        name = try_or(doc.find(
            class_="product-top__product-info__name js_product-h1-link js_product-force-scroll js_searchInGoogleTooltip default-cursor").string)
        for i in range(len(content)):
            # Local id
            l_id += 1
            # review Id
            review_id = try_or(content[i].get("data-entry-id"))
            # Author
            author = try_or(content[i].find(
                class_="user-post__author-name").string[1:])
            # Recomendation
            if try_or(content[i].find(
                class_="recommended")):
                recomendation = True
            else:
                recomendation = False
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

            data[review_id] = {
                "local_id": l_id,
                "product_id": ceneo_id, 
                "product_name": name,
                "review_Id": review_id,
                "author": author,
                "is_recomended": recomendation,
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
        n+=1
            
    Reviews.objects.create(
    local_id=data['local_id'],
    product_id=data['product_id'],
    product_name=data['product_name'],
    review_id=data['review_id'],
    author=data['author'],
    is_recomended=data['is_recomended'],
    is_verified=data['is_verified'],
    stars=data['stars'],
    date_p=datetime.strptime(data['date_p'], '%Y-%m-%d %H:%M:%S'),
    date_b=datetime.strptime(data['date_b'], '%Y-%m-%d %H:%M:%S'),
    t_up=data['t_up'],
    t_down=data['t_down'],
    opinion=data['opinion'],
    pos_features=data['pos_features'],
    neg_features=data['neg_features'],
)
# x
    
def add_product(request):
    if request.method == 'POST':
        form = Url_f(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url_f']
            scrape(url)
    else:
        form = Url_f()
    return render(request, 'main/home.html', {'form': form})

def home_p(request):
    
    context = {
        "reviews": Reviews.objects.all()
    }
    
    return render(request, 'main/home.html', context)

