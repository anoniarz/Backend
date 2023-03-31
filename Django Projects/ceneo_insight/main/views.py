from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.db.models.functions import Lower
from django.views.generic import DetailView, View
from .models import Review, Product
from datetime import datetime
from .forms import Url_f, ReviewFilterForm
from bs4 import BeautifulSoup as bs

import os
import requests
import re
import json
import collections as co


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


def scrape(link):

    flag = True
    n = 1
    ceneo_id = link_to_id(link)

    if ceneo_id == "error: 1":
        return "error: 1"

    data = {f"{ceneo_id}": {}}
    while flag:
        URL = f"https://www.ceneo.pl/{ceneo_id}/opinie-{n}"
        page = requests.get(URL)
        doc = bs(page.text, "html.parser")

        content = doc.find_all(
            class_='user-post user-post__card js_product-review')
        if content == []:
            return "error: 1"

        category = "None"
        category = try_or(doc.find(class_="js_breadcrumbs breadcrumbs").find_all(
            class_="js_breadcrumbs__item breadcrumbs__item link")[-1].text.split())
        category = " ".join(category)
        try:
            name = doc.find(
                class_="product-top__product-info__name js_product-h1-link js_product-force-scroll js_searchInGoogleTooltip default-cursor").string
        except:
            name = doc.find(
                class_="product-top__product-info__name long-name js_product-h1-link js_product-force-scroll js_searchInGoogleTooltip default-cursor").string
        if len(name) > 55:
            name = name.split(" ")
            name = " ".join(name[:5])

        rating = try_or(doc.find(
            class_="product-review").find(class_="product-review__score").get('content'))

        price = try_or(
            doc.find(class_="price-format nowrap").find(class_="value").string)

        rest = try_or(
            doc.find(class_="price-format nowrap").find(class_="penny").string)

        price = re.sub(' ', '', price)
        rest = re.sub(',', '.', rest)
        price = float(price+rest)

        for i in range(len(content)):

            review_id = try_or(content[i].get("data-entry-id"))
            author = try_or(content[i].find(
                class_="user-post__author-name").string[1:])
            # Recomendation
            try:
                recommendation = "True" if content[i].find(
                    class_="user-post__author-recomendation").find("em").string == "Polecam" else "False"
            except:
                recommendation = "None"
                pass
            # No. stars
            stars = try_or(content[i].find(
                class_="user-post__score-count").string)
            stars = re.split(r"/", stars)[0]
            stars = re.sub(',', '.', stars)
            # is_Verified
            try:
                is_verified = True if content[i].find(
                    class_="review-pz").find("em").string == "Opinia potwierdzona zakupem" else False
            except:
                is_verified = False
            # Date published
            date_p = try_or(content[i].find(
                class_="user-post__published").find_all("time")[0].get("datetime"))
            # Date Bought
            try:
                date_b = content[i].find(
                    class_="user-post__published").find_all("time")[1].get("datetime")
            except:
                date_b = date_p
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
                    pos_features = [x.string for x in fea_list[0].find_all(
                        class_="review-feature__item")]
                    neg_features = [x.string for x in fea_list[1].find_all(
                        class_="review-feature__item")]
                else:
                    neg_features = [x.string for x in fea_list[0].find_all(
                        class_="review-feature__item")]
            except:
                pass

            data[ceneo_id][review_id] = {
                "review_id": review_id,
                "author": author,
                "recommendation": recommendation,
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

    if Product.objects.filter(product_id=ceneo_id).exists():
        delete_from_db(ceneo_id)

    product = Product.objects.create(
        product_id=ceneo_id, product_category=category, product_name=name, product_rating=rating, product_price=price)

    for review_id, review in data[ceneo_id].items():
        date_p = datetime.strptime(
            review['date_p'], f'%Y-%m-%d %H:%M:%S').date()
        date_b = datetime.strptime(
            review['date_b'], f'%Y-%m-%d %H:%M:%S').date()

        time_diff = date_p - date_b
        days_used = time_diff.days

        new_review = Review.objects.create(
            product=product,
            review_id=review['review_id'],
            author=review['author'],
            recommendation=review["recommendation"],
            is_verified=review['is_verified'],
            stars=review['stars'],
            date_p=date_p,
            date_b=date_b,
            days_used=days_used,
            t_up=review['t_up'],
            t_down=review['t_down'],
            opinion=review['opinion'],
            pos_features=review['pos_features'],
            neg_features=review['neg_features'],
        )
        product.reviews.add(new_review)
    return product.pk


def add_product(request):
    if request.method == 'POST':
        form = Url_f(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url_f']
            product_id = scrape(url)
            if product_id == "error: 1":
                messages.warning(request, "Wrong ID/URL")
                previous_page = request.META.get('HTTP_REFERER')
                return redirect(previous_page)
            return redirect('product_reviews', product_id)
    else:
        form = Url_f()
    return redirect(previous_page)


def home(request):
    return render(request, 'main/home.html')


def about(request):
    return render(request, 'main/about.html')


def refresh_product(request, pk):
    scrape(str(pk))
    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page)


def delete_product(request, pk):
    delete_from_db(pk)
    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page)


class DownloadFile(View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        file_name = f'{product_id}.json'
        file_path = os.path.join(
            settings.MEDIA_ROOT, 'ceneo_reviews', file_name)

        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(), content_type='application/json')
                response['Content-Disposition'] = f'attachment; filename={file_name}'
                return response
        raise Http404


def products(request):

    products = Product.objects.all()

    user = request.user
    user_favourites_list = []
    if user.is_authenticated:
        user_favourites = request.user.profile.favourites.all()
        user_favourites_list = [
            product.product_id for product in user_favourites]

    category = request.GET.get('category')
    if category != "None" and category != "All":
        products = products.filter(product_category=category)

    categories = Product.objects.values_list(
        'product_category', flat=True).distinct()

    sorter = request.GET.get('sort')
    if sorter == 'a-z':
        products = products.order_by(Lower('product_name'))
    elif sorter == 'z-a':
        products = products.order_by(Lower('product_name').desc())
    elif sorter == 'most_reviews':
        products = sorted(
            products, key=lambda p: p.reviews.count(), reverse=True)
    elif sorter == 'least_reviews':
        products = sorted(products, key=lambda p: p.reviews.count())
    elif sorter == 'highest_rating':
        products = products.order_by('-product_rating')
    elif sorter == 'lowest_rating':
        products = products.order_by('product_rating')
    elif sorter == 'highest_price':
        products = products.order_by('-product_price')
    elif sorter == 'lowest_price':
        products = products.order_by('product_price')

    paginator = Paginator(products, 14)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "sorter": sorter,
        'user_favourites_list': user_favourites_list,
        "categories": categories,
        "selected_category": category,
    }
    return render(request, 'main/products.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product_reviews.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        product = self.get_object()
        reviews = Review.objects.filter(product_id=product.product_id)

        stars_numbers = sorted(set([float(x.stars) for x in reviews]))
        recommend_options = sorted(set([x.recommendation for x in reviews]))

        form = ReviewFilterForm(self.request.GET or None)

        if form.is_valid():

            data = form.cleaned_data
            stars = data.get('stars')
            recommendation = data.get('recommendation')
            is_verified = data.get('is_verified')
            days_used = data.get('days_used')
            t_up = data.get('t_up')
            t_down = data.get('t_down')
            pos_feat = data.get('pos_features')
            neg_feat = data.get('neg_features')

            if stars:
                for i in range(len(stars)):
                    if float(stars[i]) % 1 == 0:
                        stars[i] = str(stars[i])[0]
                reviews = reviews.filter(stars__in=stars)

            if recommendation:
                reviews = reviews.filter(recommendation__in=recommendation)
            if is_verified:
                reviews = reviews.filter(is_verified=is_verified)
            if days_used:
                reviews = reviews.filter(days_used__gte=days_used)
            if t_up:
                reviews = reviews.filter(t_up__gte=t_up)
            if t_down:
                reviews = reviews.filter(t_down__lte=t_down)

            if pos_feat:
                pos_feat_list = []
                for review in reviews:
                    if len(review.pos_features) >= pos_feat:
                        pos_feat_list.append(review.review_id)
                reviews = reviews.filter(review_id__in=pos_feat_list)

            if neg_feat:
                neg_feat_list = []
                for review in reviews:
                    if len(review.neg_features) >= neg_feat:
                        neg_feat_list.append(review.review_id)
                reviews = reviews.filter(review_id__in=neg_feat_list)

        sorter = self.request.GET.get('sort')
        if sorter == 'newest':
            reviews = reviews.order_by('-date_p')
        elif sorter == 'oldest':
            reviews = reviews.order_by('date_p')
        elif sorter == 'highest_rated':
            reviews = reviews.order_by('-stars')
        elif sorter == 'lowest_rated':
            reviews = reviews.order_by('stars')
        elif sorter == 'most_liked':
            reviews = reviews.order_by('-t_up')
        elif sorter == 'most_disliked':
            reviews = reviews.order_by('-t_down')
        elif sorter == 'most_used':
            reviews = reviews.order_by('-days_used')
        elif sorter == 'pos_features':
            reviews = sorted(
                reviews, key=lambda p: len(p.pos_features), reverse=True)
        elif sorter == 'neg_features':
            reviews = sorted(
                reviews, key=lambda p: len(p.neg_features), reverse=True)

        paginator = Paginator(reviews, 7)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        chart_stars = co.Counter(
            sorted([x.stars for x in reviews], reverse=True))
        chart_recommendations = co.Counter(
            sorted([x.recommendation for x in reviews], reverse=True))
        days_used = co.Counter(sorted([x.days_used for x in reviews]))

        context = {
            'labels1': list(chart_stars.keys()),
            'values1': list(chart_stars.values()),
            'labels2': list(chart_recommendations.keys()),
            'values2': list(chart_recommendations.values()),
            'labels3': list(days_used.keys()),
            'values3': list(days_used.values()),
            'product': product,
            'reviews': page_obj,
            'sorter': sorter,
            'filter_form': form,
            'stars_numbers': stars_numbers,
            'recommend_options': recommend_options,
        }
        return context
