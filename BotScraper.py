import json
from warnings import catch_warnings
from bs4 import BeautifulSoup

import requests

url = 'https://webscraper.io/test-sitess/e-commerce/allinone/computers/laptops'

try:
    html = requests.get(url)
    html.status_code == 200
    html.raise_for_status()
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)
else:
    soup = BeautifulSoup(html.content, 'html.parser')

    elementsPrices = soup.find_all("h4", class_="pull-right price")
    elementsTitles = soup.find_all("a", attrs={"class": "title"})
    
    prices = []
    titles = []
    notebooks = []
    searched = 'Asus'

    for price in elementsPrices:
        prices.append(price.text)

    for title in elementsTitles:
        titles.append(title.get('title'))

    for i in range(0, len(elementsPrices)-1):
        notebooks.append({"Title": titles[i], "Price": prices[i]})

    notebookFiltrado = [notebook for notebook in notebooks if notebook['Title'].count(searched)]

    with open('dados.json', 'w') as json_file:    
        json.dump(notebookFiltrado, json_file, indent=4)