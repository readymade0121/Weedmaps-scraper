import pandas as pd
import requests
from time import sleep
from csv import writer
from lib2to3.pgen2 import driver
from urllib import response
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np

options={
    'proxy':{
        "http": "http://arpkmgvp-rotate:jh3269dn5f@p.webshare.io:80/",
        "https": "http://arpkmgvp-rotate:jh3269dn5f@p.webshare.io:80/",
        "no_proxy": 'localhost,127.0.0.1'

    }
}

url = 'https://weedmaps.com/search?page={}'

ua = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': 'PostmanRuntime/7.26.8', 'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive'}
page_number = 5

product_suburls = []
product_suburl = ''
types = []
names = []
thc = []
cbd = []
prices = []
sizes = []
images = []
brands = []

driver = webdriver.Chrome(executable_path='./chromedriver.exe', seleniumwire_options=options)
driver.maximize_window()
sleep(40)
for x in range(page_number):
    product_url = url.format(x+1)
    # response = requests.get(brand_url, headers=headers)
    # brand = json.loads(response.text)['data']['brands']
    driver.get(product_url)
    products = driver.find_elements(By.CLASS_NAME, 'base-card__Info-sc-1fhygl1-4')
    for product in products:
        product_suburl = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
        
        product_suburls.append(product_suburl[:product_suburl.index('?')])
        type_span = product.find_element(By.CLASS_NAME, 'styles__CategoryContainer-sc-j5iyiv-2')
        type = type_span.find_element(By.TAG_NAME, 'span').text
        types.append(type)
        brand = product.find_element(By.CLASS_NAME, 'styles__BrandContainer-sc-j5iyiv-0').text
        brands.append(brand)

        name = product.find_element(By.CLASS_NAME, 'base-card__Title-sc-1fhygl1-5').text
        names.append(name)
        
        thc_cbd = product.find_elements(By.CLASS_NAME, 'chip__StyledChip-sc-ivkx98-0')
        if(thc_cbd):
            for x in thc_cbd:
                cha = x.text
                # print(cha[-3:])
                if(cha[-3:] == 'THC'):
                    thc.append(cha.replace(cha[-3:],''))
                else:
                    cbd.append(cha.replace(cha[-3:],''))
        else:
            thc.append('')
            cbd.append('')

        price = product.find_element(By.CLASS_NAME, 'styles__PriceText-sc-2i2drq-1').text
        prices.append(price)

        size = product.find_element(By.CLASS_NAME,'gYaRZB').text
        sizes.append(size)

        # image = product.find_element(By.TAG_NAME,'img').get_attribute('src')
        # images.append(image)
    image = driver.find_elements(By.CLASS_NAME , 'img-component')

    for y in image:
        images.append(y.get_attribute('src'))


with open('urls.txt', 'w') as f:
    f.write('\n'.join(product_suburls))
# print(types,names,thc,cbd,prices,sizes,images)           

count1=0
i=0
# driver.get('https://weedmaps.com/brands/khalifa-kush/products/khalifa-kush-flower?filter%5BanyWeights%5D%5Bounce%5D%5B0%5D=1%2F8&filter%5BboundingRadius%5D=50mi&boost%5Blisting_wmid%5D=241456909&origin=search')
# try:
#     brand = driver.find_element(By.CLASS_NAME, 'brand-product-header__BrandName-sc-1yu4kvg-0').text
# except:
#     brand = ''
# product_suburls=np.loadtxt("input.txt", dtype="str")

# print(brand)
# for x in product_suburls:
#     dispen = []
#     driver.get(x[i])

#     try:
#         brand = driver.find_element(By.CLASS_NAME, 'brand-product-header__BrandName-sc-1yu4kvg-0').text
#     except:
#         brand = ''
#     # print(brand)

#     try:
#         dispensaris = driver.find_elements(By.CLASS_NAME, 'styles__ListingName-sc-aykab1-0')
#         for dispensary in dispensaris:
#             dispen.append(dispensary.text)
#     except:
#         dispen = ''
#     try:
#         driver.find_element(By.CLASS_NAME, 'styles__AccordionArrow-sc-7ycru1-0').click()
#         sleep(5)
#         description = driver.find_element(By.CLASS_NAME,'styles__ProductBodyCopy-sc-1gm6n5v-0').text
#     except:
#         description = ''
    # print(brand, dispen, description)

row = [brand[i], names[i], types[i], thc[i], cbd[i], sizes[i], prices[i], images[i]]
i = i+1

with open('product_1.csv', 'a', encoding='utf-8', newline='') as f_object:
    product_row = writer(f_object)
    count1 = count1 + 1
    if count1 == 1:
        product_row.writerow(['brand', 'name', 'type', 'thc','cbd', 'size', 'price', 'image'])
    product_row.writerow(row)
    f_object.close()

    
