import json

from bs4 import BeautifulSoup
import requests
from datetime import datetime
import sys

url = "https://www.castorama.ru/catalogue"

headers = {
    "Accept": "*/*",
    "Accept-encoding": "gzip, deflate, br",
    "Accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",

    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 OPR/78.0.4093.147"

}


def create_request():
    req = requests.get(url, headers=headers)
    src = req.text
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(src)


with open("index.html", encoding="utf-8") as file:
    src = file.read()


def create_categories():
    soup = BeautifulSoup(src, "lxml")
    all_products_hrefs = soup.find_all(class_="category__link")

    all_products_dict = {}
    for item in all_products_hrefs:
        item_text = item.text
        item_href = item.get("href")

        all_products_dict[item_text] = item_href

    with open("all_categories_dict.json", "w", encoding="utf-8") as file:
        json.dump(all_products_dict, file, indent=4, ensure_ascii=False)


def create_categories_files():
    with open("all_categories_dict.json", encoding="utf-8") as file:
        all_categories = json.load(file)

    for category_name, category_href in all_categories.items():

        rep = [" ", "\n"]
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, "")

        req = requests.get(url=category_href, headers=headers)
        src = req.text
        with open(f"data/{datetime.now().date()} {category_name}.html", "w", encoding="utf-8") as file:
            file.write(src)

create_categories_files()