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

options={
    'proxy':{
        "http": "http://arpkmgvp-rotate:jh3269dn5f@p.webshare.io:80/",
        "https": "http://arpkmgvp-rotate:jh3269dn5f@p.webshare.io:80/",
        "no_proxy": 'localhost,127.0.0.1'

    }
}


url = 'https://api-g.weedmaps.com/discovery/v1/brands?filter%5Blatlng%5D=38.88825%2C-77.06938&filter%5Buse_geoip%5D=true&filter%5Bnew_market%5D=false&filter%5Bbounding_radius%5D=50mi&sort_by=recommended&include%5B%5D=brand.nearby_deals_count&include%5B%5D=brand.in_new_market&page_size=24&page={}'

ua = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': 'PostmanRuntime/7.26.8', 'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive'}
page_number = 40
brand_slugs = []
brand_names = []
for x in range(page_number):
    brand_url = url.format(x+1)
    response = requests.get(brand_url, headers=headers)
    brand = json.loads(response.text)['data']['brands']
    for y in brand:
        brand_slugs.append(y['slug'])
        brand_names.append(y['name'])
# print(len(product_names))

driver = webdriver.Chrome(executable_path='./chromedriver.exe', seleniumwire_options=options)
driver.maximize_window()

brand_baseurl1 = 'https://weedmaps.com/brands/{}/discover'
brand_baseurl2 = 'https://weedmaps.com/brands/{}/feed'
count = 0
for brand_slug in brand_slugs:
    driver.get(brand_baseurl1.format(brand_slug))
    # items = driver.find_elements(By.CLASS_NAME, "dyjEub")
    try:
        details = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//section[1]/div/div[3]'))).text
        # details = driver.find_element(By.XPATH, '//section[1]/div/div[3]').text
        # print(details)
        if details == '':
            details = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//section[1]/div/div[2]'))).text
            # details = driver.find_element(By.XPATH, '//section[1]/div/div[2]').text
    except:
        details = ''
    try:
        license = driver.find_element(By.XPATH, '//section[2]/ul').text
    except:
        license = ''
    try: 
        image = driver.find_element(By.XPATH, '//picture[1]/img').get_attribute('src')
        # print(image)
    except:
        image = ''
    
    driver.get(brand_baseurl2.format(brand_slug))
    instagram = ''
    twitter = ''
    facebook = ''
    website = ''
    other = ''
    try:
        social = driver.find_elements(By.CLASS_NAME, 'brand-social-links__SocialLink-sc-pohbyq-1')
        for span in social:
            if span.text == "Instagram":
                instagram = span.get_attribute('href')
            elif span.text == "Twitter":
                twitter = span.get_attribute('href')
            elif span.text == "Facebook":
                facebook = span.get_attribute('href')
            elif span.text == "Website":
                website = span.get_attribute('href')
            else:
                other = span.get_attribute('href')
    except:
        instagram = ''
        twitter = ''
        facebook = ''
        website = ''
        other = ''      
        
    # section = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'section')))
    row = [brand_names[count], facebook, instagram, twitter, website, other, details, license, image]
    with open('brands_final.csv', 'a', encoding='utf-8', newline='') as f_object:
        product_row = writer(f_object)
        count = count + 1
        if count == 1:
            product_row.writerow(['Name', 'FaceBook', 'Instagram', 'Twitter','Website', 'Other', 'Details', 'License', 'ImageURL'])
        product_row.writerow(row)
        f_object.close()
