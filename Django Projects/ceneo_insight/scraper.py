links = [
    "https://www.ceneo.pl/133337315#tab=reviews",
    "https://www.ceneo.pl/123854584",
    "https://www.ceneo.pl/113798881",
    "https://www.ceneo.pl/136848772",
    "https://www.ceneo.pl/50367847",
]

def link_to_id(adress):
    import re
    return "".join(re.findall(r"\d+", adress))

def scrape(link):
    import requests
    from bs4 import BeautifulSoup as bs
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
            
    return data


for link in links:
    import json
    ceneo_id = link_to_id(link) 
    data = scrape(ceneo_id)
    with open(f'ceneo_reviews\{ceneo_id}.json', 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
