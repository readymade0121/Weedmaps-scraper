import pandas as pd
import requests
import json
from csv import writer
from lib2to3.pgen2 import driver
from urllib import response
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

product_origin_url = "https://api-g.weedmaps.com/discovery/v1/products?"
product_page_per_take = 100  # 18
product_page_num = 100

productList_slug = []
productList_name = []
productList_url = []
productList_category = []
productList_thc = []
productList_cbd = []
productList_review_count = []
productList_desc = []
productList_rating = []
productList_price = []

ua = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': 'PostmanRuntime/7.26.8', 'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive'}


def scrapProducts():

    for x in range(product_page_num):
        product_get_url = (
            product_origin_url + "&page={}&page_size={}&latlng=33.83475%2C-117.91173").format(x+1, product_page_per_take)
        # print(product_get_url)
        response = requests.get(product_get_url, headers=headers)
        # print(response.text)
        products = json.loads(response.text)['data']['products']
        for y in products:
            productList_slug.append(y['slug'])
            productList_name.append(y['name'])
            productList_url.append(y['avatar_image_url'])
            productList_review_count.append(y['reviews_count'])
            productList_thc.append(y['variant']['aggregate_metrics']['thc'])
            productList_cbd.append(y['variant']['aggregate_metrics']['cbd'])
            try:
                productList_desc.append(y['brand']['description'])
            except:
                productList_desc.append('')

            productList_rating.append(y['rating'])
            productList_price.append(y['variant']['price']['price'])
       
scrapProducts()
df = pd.DataFrame({
    'name': productList_name,
    'slug': productList_slug,
    'url': productList_url,
    'thc': productList_thc,
    'cbd': productList_cbd,
    'rating': productList_rating,
    'review_count': productList_review_count,
    'description': productList_desc,
    'price': productList_price,

})
df.to_excel('weed_product.xlsx', index=False, encoding='utf-8')
print('weedmap_product_done')

