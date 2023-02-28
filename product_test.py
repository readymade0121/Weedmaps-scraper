import pandas as pd
import requests
import json
from csv import writer
from lib2to3.pgen2 import driver
from urllib import response
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep


product_origin_url = "https://api-g.weedmaps.com/discovery/v1/products?"
product_page_per_take = 100  # 18
product_page_num = 100


ua = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': 'PostmanRuntime/7.26.8', 'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive'}
i = 0
for x in range(product_page_num):
    product_get_url = (
        product_origin_url + "&page={}&page_size={}&latlng=33.83475%2C-117.91173").format(x+1, product_page_per_take)
    # print(product_get_url)
    try:
        response = requests.get(product_get_url, headers=headers)
    except requests.exceptions.ReadTimeout:
        print('timeout')
        sleep(3)
    # print(response.text)
    products = json.loads(response.text)['data']['products']
    # sleep(2)
    for y in products:
        try:
            productList_brand = y['brand']['name']
        except:
            productList_brand = ''
        productList_name = y['name']
        try:
            productList_type = y['edge_category']['name']
        except:
            productList_type = ''

        productList_thc = y['variant']['aggregate_metrics']['thc']
        productList_cbd = y['variant']['aggregate_metrics']['cbd']
        try:
            productList_desc = y['brand']['description']
        except:
            productList_desc = ''

        productList_unit = y['variant']['price']['label']
        productList_price = y['variant']['price']['price']
        productList_image = y['avatar_image_url']
        row = [productList_brand, productList_name, productList_type, productList_thc, productList_cbd, productList_desc, productList_unit, productList_price, productList_image]
        

        with open('product.csv', 'a', encoding='utf-8', newline='') as f_object:
            product_row = writer(f_object)
            i = i+1
            if i == 1:
                product_row.writerow(['brand', 'name', 'type', 'thc','cbd', 'size', 'price', 'image'])
            product_row.writerow(row)
            f_object.close()
       
# scrapProducts()


