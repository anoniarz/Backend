from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.conf import settings
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.contrib import messages
from .models import Review, Product
from datetime import datetime, timedelta
from .forms import Url_f


from django.views.generic import DetailView, View
# Scraper
import os
import requests
import re
import json
import collections as co
from bs4 import BeautifulSoup as bs


def delete_from_db(ceneo_id):
    Product.objects.filter(product_id=ceneo_id).delete()


def link_to_id(adress):
    return "".join((re.findall(r"\d{5,}", adress))[0])


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
    chart_stars = []
    chart_recommendations = []
    while flag:
        URL = f"https://www.ceneo.pl/{ceneo_id}/opinie-{n}"
        page = requests.get(URL)
        doc = bs(page.text, "html.parser")
        content = doc.find_all(
            class_='user-post user-post__card js_product-review')
        if content == []:
            return "error: 1"

        product_name = try_or(doc.find(
            class_="product-top__product-info__name js_product-h1-link js_product-force-scroll js_searchInGoogleTooltip default-cursor").string)
        rating = try_or(doc.find(class_="product-review").find(class_="product-review__score").get('content'))
        # Scraping
        for i in range(len(content)):
            local_id += 1
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
            chart_recommendations.append(recommendation)
            # No. stars
            stars = try_or(content[i].find(
                class_="user-post__score-count").string)
            stars = re.split(r"/", stars)[0]
            stars = re.sub(',', '.', stars)
            chart_stars.append(float(stars))
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
            try:
                date_b = content[i].find(class_="user-post__published")
                date_b = date_b.find_all("time")[1].get("datetime")
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
                "local_id": local_id,
                "product_id": ceneo_id,
                "product_name": product_name,
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

    # Chart Data
    chart_stars = co.Counter(sorted(chart_stars, reverse=True))
    chart_recommendations = co.Counter(
        sorted(chart_recommendations, reverse=True))

    # Saving Data as Json
    with open(f'media\ceneo_reviews\{ceneo_id}.json', 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    # Adding Data to DataBase
    if Product.objects.filter(product_id=ceneo_id).exists():
        delete_from_db(ceneo_id)

    product_name = data[ceneo_id][review_id].get('product_name')
    product = Product.objects.create(
                                     product_id=ceneo_id, product_name=product_name, chart_stars=chart_stars, chart_recommendations=chart_recommendations, rating=rating)

    for review_id, review in data[ceneo_id].items():
        date_p = datetime.strptime(
            review['date_p'], f'%Y-%m-%d %H:%M:%S').date()
        date_b = datetime.strptime(
            review['date_b'], f'%Y-%m-%d %H:%M:%S').date()
        
        time_diff = date_p - date_b
        days_used = time_diff.days
  
        new_review = Review.objects.create(
            product=product,
            local_id=review['local_id'],
            review_id=review['review_id'],
            author=review['author'],
            recommendation=review["recommendation"],
            is_verified=review['is_verified'],
            stars=review['stars'],
            date_p=date_p,
            date_b=date_b,
            days_used = days_used,
            t_up=review['t_up'],
            t_down=review['t_down'],
            opinion=review['opinion'],
            pos_features=review['pos_features'],
            neg_features=review['neg_features'],
        )
        product.reviews.add(new_review)
    return product.pk


def error(request):
    return render(request, 'main/error.html')

# Adding Product
def add_product(request):
    if request.method == 'POST':
        form = Url_f(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url_f']
            product_pk = scrape(url)
            if product_pk == "error: 1":
                messages.warning(request, "Wrong ID/URL")
                return redirect('add_product')
            return redirect('product_reviews', product_pk)
    else:
        form = Url_f()
    return render(request, 'main/add_product.html', {'form': form})


def home(request):
    return render(request, 'main/home.html')


def about(request):
    return render(request, 'main/about.html')


def refresh_product(request, pk):
    scrape(str(pk))
    return redirect('products')


def delete_product(request, pk):
    delete_from_db(pk)
    return redirect('products')


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
    sort_by = request.GET.get('sort_by')
    products = Product.objects.all()

    if sort_by == 'a-z':
        products = products.order_by('product_name')
    elif sort_by == 'z-a':
        products = products.order_by('-product_name')
    elif sort_by == 'most_reviews':
        products = sorted(products, key=lambda p: p.reviews.count(), reverse=True)
    elif sort_by == 'least_reviews':
        products = sorted(products, key=lambda p: p.reviews.count())
    elif sort_by == 'highest_rating':
        products = products.order_by('-rating')
    elif sort_by == 'lowest_rating':
        products = products.order_by('rating')
        
    request.session['sort_by'] = sort_by

    context = {
        "products": products,
        "sort_by": sort_by,
    }

    return render(request, 'main/products.html', context)


class ProductDetailView(DetailView):
    model = Product
    paginate_by = 7
    template_name = 'main/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.get_object()
        reviews = product.reviews.all()
        days_used = []
        for review in reviews:
            if review.days_used <= 10:
                days_used.append("1+")
            elif review.days_used <= 20:
                days_used.append("10+")
            elif review.days_used <= 30:
                days_used.append("20+")
            elif review.days_used <= 40:
                days_used.append("30+")
            elif review.days_used > 40:
                days_used.append("40+")
        days_used = co.Counter(sorted(days_used))

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

        paginator = Paginator(reviews, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['labels1'] = list(product.chart_stars.keys())
        context['values1'] = list(product.chart_stars.values())
        context['labels2'] = list(product.chart_recommendations.keys())
        context['values2'] = list(product.chart_recommendations.values())
        context['labels3'] = list(days_used.keys())
        context['values3'] = list(days_used.values())
        context['reviews'] = page_obj
        context['sorter'] = sorter

        context['sort_links'] = {
            'Newest': reverse('product_reviews', args=[product.pk]) + '?sort=newest',
            'Oldest': reverse('product_reviews', args=[product.pk]) + '?sort=oldest',
            'Highest_Rated': reverse('product_reviews', args=[product.pk]) + '?sort=highest_rated',
            'Lowest_Rated': reverse('product_reviews', args=[product.pk]) + '?sort=lowest_rated',
            'Most_Liked': reverse('product_reviews', args=[product.pk]) + '?sort=most_liked',
            'Most_Disliked': reverse('product_reviews', args=[product.pk]) + '?sort=most_disliked',
            'Most_Used': reverse('product_reviews', args=[product.pk]) + '?sort=most_used',
        }
        return context
