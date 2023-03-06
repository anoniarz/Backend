import requests
import json
from bs4 import BeautifulSoup as bs


def try_or(f):
    try:
        return f
    except:
        return None


data = {}


for n in range(1, 9):
    URL = f"https://www.ceneo.pl/94823130/opinie-{n}"
    page = requests.get(URL)
    doc = bs(page.text, "html.parser")
    print(doc)

    content = doc.find_all(
        class_='user-post user-post__card js_product-review')
    try_or(name=doc.find(
        class_="product-top__product-info__name js_product-h1-link js_product-force-scroll js_searchInGoogleTooltip default-cursor").string)

    with open('content.json', 'w', encoding="utf-8") as file:

        for i in range(len(content)):
            l_id = i+1
            # review Id
            review_id = try_or(content[i].get("data-entry-id"))
            # Author
            author = try_or(content[i].find(
                class_="user-post__author-name").string[1:])
            # Recomendation
            recomendation = try_or(True if content[i].find(
                class_="user-post__author-recomendation").string == "Polecam" else False)
            # No. stars
            stars = try_or(content[i].find(
                class_="user-post__score-count").string)
            # is_Verified
            try:
                is_verified = True if content[i].find(
                    class_="review-pz").find("em").string == "Opinia potwierdzona zakupem" else False
            except:
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
                "product_name": name,
                "Id": review_id,
                "author": author,
                "is_recomended": recomendation,
                "stars": stars,
                "is_verified": is_verified,
                "date_p": date_p,
                "date_b": date_b,
                "t_up": t_up,
                "t_down": t_down,
                "opinion": opinion,
                "features": {"positive": pos_features, "negative": neg_features}
            }
        json.dump(data, file, indent=4, ensure_ascii=False)
