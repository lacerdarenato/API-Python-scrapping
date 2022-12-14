from bs4 import BeautifulSoup

import json
import requests

def scraping(searched):
    url = 'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops'

    try:
        html = requests.get(url)
        html.status_code == 200
        html.raise_for_status()

        soup = BeautifulSoup(html.content, 'html.parser')
        elementsPrices = soup.find_all("h4", class_="pull-right price")
        elementsDescriptions = soup.find_all("p", class_="description")
        elementsTitles = soup.find_all("a", attrs={"class": "title"})
        elementsReviews = soup.find_all("p", class_="pull-right") 
        elementsRatings = soup.find_all("div", class_="ratings")# conferir pq não funciona? ("p", attrs={"class": "data-rating"})


        prices = []
        descriptions = []
        titles = []
        productIds = []
        ratings = []
        reviews = []
        notebooks = []

        for price in elementsPrices:
            prices.append(float(price.text[1:]))

        for description in elementsDescriptions:
            descriptions.append(description.text)

        for title in elementsTitles:
            titles.append(title.get('title'))
            productIds.append(int(title.get('href').split('/')[-1]))
        
        for review in elementsReviews:
            reviews.append(review.text)

        for rating in elementsRatings:
            ratings.append(rating.get('data-rating'))

        for i in range(0, len(elementsPrices)-1):
            notebooks.append({"productId": productIds[i], "title": titles[i], "price": prices[i], "description": descriptions[i], "review": reviews[i], "rating": 0}) #, "Ratings": ratings[i]
        notebookFiltrado = [notebook for notebook in notebooks if notebook['title'].count(searched)]
        notebookInOrder = sorted(notebookFiltrado, key=lambda notebook: notebook['price'])

        try: 
            json_file = open('dados.json', 'w')
            json.dump(notebookInOrder, json_file, indent=4)
            json_file.close()
        except OSError as err:
            print("OS Error: {0}".format(err))
        return {"message":"Encontrado " + searched + " via scraping"}, 200
            
        
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)