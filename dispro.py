import pandas as pd
import requests
import json
from csv import writer
from lib2to3.pgen2 import driver
from urllib import response
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
print('start')
options={
    'proxy':{
        "http": "http://arpkmgvp-rotate:jh3269dn5f@p.webshare.io:80/",
        "https": "http://arpkmgvp-rotate:jh3269dn5f@p.webshare.io:80/",
        "no_proxy": 'localhost,127.0.0.1'

    }
}

url = 'https://weedmaps.com/dispensaries/in/canada/ontario/toronto-east?page={}'

ua = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': 'PostmanRuntime/7.26.8', 'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive'}
page_number = 8
brand_slugs = []
despensaries_suburls = []
despensaries_suburl = ''
country = "Canada"
driver = webdriver.Chrome(executable_path='./chromedriver.exe', seleniumwire_options=options)
driver.maximize_window()

for x in range(page_number):
    despensaries_url = url.format(x+1)

    driver.get(despensaries_url)
    despensaries = driver.find_elements(By.CLASS_NAME, 'base-card__Info-sc-1fhygl1-4')
    for despensary in despensaries:
        try:
            despensaries_suburl = despensary.find_element(By.TAG_NAME, 'a').get_attribute('href')
        except:
            break
        if(despensaries_suburl):
            despensaries_suburls.append(despensaries_suburl)
count1=0

for x in despensaries_suburls:
    page = 0
    pro_names = []
    product_url =  x + "?page={}"
    try:
        dis_name = driver.find_element(By.TAG_NAME, 'h1').text
    except:
        dis_name = ''
    while 1:
        # real_url = url.format(page+1)
        driver.get(product_url.format(page + 1))
        page = page + 1

        name_div = driver.find_elements(By.CLASS_NAME, 'base-card__Title-sc-1fhygl1-5')
        if len(name_div) == 0:
            break
        else:
            for name in name_div:
                pro_names.append(name.text)
                print(dis_name, "--Pro_name--", name.text)


    row = [dis_name, pro_names]
    with open('dispro.csv', 'a', encoding='utf-8', newline='') as f_object:
        product_row = writer(f_object)
        count1 = count1 + 1
        if count1 == 1:
            product_row.writerow(['DispensaryName', 'ProductName'])
        product_row.writerow(row)
        f_object.close()
