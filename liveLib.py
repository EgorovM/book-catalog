# IMPORTS
from skimage.io import imread
from bs4 import BeautifulSoup
import pandas as pd
import requests

import time, random

from fake_useragent import UserAgent

URL = "https://www.livelib.ru/reviews/~%d#reviews"

def extract_reviews(parser):
    reviews_list = []
    
    reviews_divs = parser.find_all("article", {"class": "review-card"})
    
    for ind in range(len(reviews_divs)):
        try:
            label          = float(reviews_divs[ind].find("span", {"class": "lenta-card__mymark"}).text)
            review_content = get_name(reviews_divs[ind].find("div",  {"class": "lenta-card__text"}))
            
            review = {
                "content" : review_content, 
                "label" : label
            }

            reviews_list.append(review)
        except:
            print("ASD")
        
    return reviews_list


def get_name(parser):
    text = ""
    
    for p in parser.find_all("p"):
        text += p.text
        
    return text


def get_reviews_from_livelib(n_pages=1):
    reviews = []

    while n_pages:
        reviews_list = []
        
        response = requests.get(URL % n_pages, headers={'User-Agent': UserAgent().chrome})
        response.encoding = response.apparent_encoding
        print(response.url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        reviews.extend(extract_reviews(soup))
        time.sleep(1 + random.randint(0, 20) / 10)
        n_pages -= 1
    
    return reviews

a = get_reviews_from_livelib(10)

data = pd.DataFrame(a)

data.to_csv("kino_reviews.csv", index=None)