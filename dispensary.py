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
    # response = requests.get(brand_url, headers=headers)
    # brand = json.loads(response.text)['data']['brands']
    driver.get(despensaries_url)
    despensaries = driver.find_elements(By.CLASS_NAME, 'base-card__Info-sc-1fhygl1-4')
    for despensary in despensaries:
        try:
            despensaries_suburl = despensary.find_element(By.TAG_NAME, 'a').get_attribute('href')
        except:
            break
        if(despensaries_suburl):
            despensaries_suburls.append(despensaries_suburl+"/about")
count1=0

for x in despensaries_suburls:
    driver.get(x)
# driver.get('https://weedmaps.com/dispensaries/wonderland-cannabis/about')

    try:
        name = driver.find_element(By.TAG_NAME, 'h1').text
    except:
        name = ''
    try:
        image = driver.find_element(By.TAG_NAME, 'img').get_attribute('src')
    except:
        image = ''
    # print(image)
    try:
        address_all = driver.find_elements(By.CLASS_NAME, 'styled-components__AddressRow-sc-1god7hx-2')
    except:
        address_all = ''

    count = 0

    for y in address_all:
        count = count + 1
        if(count == 1):
            address = y.text
        elif(count == 2):
            city = y.text

    try:
            
        googlemap = driver.find_element(By.CLASS_NAME, 'styled-components__AddressLink-sc-1god7hx-3').get_attribute('href')
    except:
        googlemap = ''

    
    try:
        week = driver.find_elements(By.CLASS_NAME, 'styles__Range-sc-17covz-14')
    except:
        week = ''

    week_count = 0

    mon = ''
    tue = ''
    wed = ''
    thu = ''
    fri = ''
    sat = ''
    sun = ''

    for z in week:
        match week_count:
            case 1:
                mon = z.text
            case 2:
                tue = z.text
            case 3:
                wed = z.text
            case 4:
                thu = z.text
            case 5:
                fri = z.text
            case 6:
                sat = z.text
            case 7:
                sun = z.text
        week_count = week_count + 1

    inds = driver.find_elements(By.CLASS_NAME,'header-info__ListingInfoLine-sc-1heoxjr-2')
    online_shop = ''
    store_front = ''
    recreational = ''
    medical = ''
    curbside = ''
    accessible = ''
    security = ''
    for ind in inds:
        match ind.text:
            case 'Order online (pickup)':
                online_shop = 'Y'
            case 'In-store purchases only':
                online_shop = 'Y'
            case 'Storefront':
                store_front = 'Y'
            case 'Recreational':
                recreational = 'Y'
            case 'Medical':
                medical = 'Y'
            case 'Curbside pickup':
                curbside = 'Y'
            case 'Accessible':
                accessible = 'Y'
            case 'Security':
                security = 'Y'
    # print('mon',mon, 'tue', tue,'wed', wed)
    try:
        phone = driver.find_element(By.CLASS_NAME,'header-info__DesktopButtonContent-sc-1heoxjr-1').text
    except:
        phone = ''
    try:
        mail = driver.find_element(By.CLASS_NAME,'styled-components__Email-sc-5o6q5l-3').text
    except:
        mail = ''
    try:
        website = driver.find_element(By.CLASS_NAME,'styled-components__Website-sc-5o6q5l-4')
    except:
        website = ''
    try:
        website_url = website.find_element(By.TAG_NAME,'a').get_attribute('href')
    except:
        website_url = ''
    try:
        social_class = driver.find_element(By.CLASS_NAME,'styled-components__SocialMedia-sc-5o6q5l-5')
    except:
        social_class = ''
    try:
        social_urls = social_class.find_elements(By.TAG_NAME, 'a')
    except:
        social_urls = ''

    facebook =''

    instagram = ''

    twitter = ''

    for social_url in social_urls:
        print(social_url.text)
        if(social_url.text == 'Facebook'):
            try:
                facebook = social_url.get_attribute('href')
            except:
                facebook = ''
        elif(social_url.text == '@Instagram'):

            try:
                instagram =  social_url.get_attribute('href')
            except:
                instagram = ''
        else:
            try:
                twitter = social_url.get_attribute('href')
            except:
                twitter = ''
        
    try:
        license_div = driver.find_element(By.CLASS_NAME,'styled-components__LicenseSection-sc-70slo8-6')
        license = license_div.find_element(By.TAG_NAME, "span").text
    except:
        license = ''

    row = [name, address, city, country, phone,mail, website_url, facebook, instagram, twitter, googlemap, license, mon, tue, wed, thu, fri, sat, sun, online_shop, store_front, recreational, medical, curbside, accessible, security, image]
    
    with open('dispensary.csv', 'a', encoding='utf-8', newline='') as f_object:
        product_row = writer(f_object)
        count1 = count1 + 1
        if count1 == 1:
            product_row.writerow(['Name', 'Address', 'city', 'country','phone', 'email','website', 'facebook', 'instagram', 'twitter', 'googlemap', 'license','mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'image', 'Online_Shop', 'StoreFront', 'Recreational','Medical','Curbside_Pickup','Accessible','Security'])
        product_row.writerow(row)
        f_object.close()

  


    # print(despensaries_suburls)

# driver = webdriver.Chrome(executable_path='./chromedriver.exe', seleniumwire_options=options)
# driver.maximize_window()

# brand_baseurl1 = 'https://weedmaps.com/brands/{}/discover'
# brand_baseurl2 = 'https://weedmaps.com/brands/{}/feed'
# count = 0
# for brand_slug in brand_slugs:
#     driver.get(brand_baseurl1.format(brand_slug))
#     # items = driver.find_elements(By.CLASS_NAME, "dyjEub")
#     try:
#         details = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//section[1]/div/div[3]'))).text
#         # details = driver.find_element(By.XPATH, '//section[1]/div/div[3]').text
#         # print(details)
#         if details == '':
#             details = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//section[1]/div/div[2]'))).text
#             # details = driver.find_element(By.XPATH, '//section[1]/div/div[2]').text
#     except:
#         details = ''
#     try:
#         license = driver.find_element(By.XPATH, '//section[2]/ul').text
#     except:
#         license = ''
#     try: 
#         image = driver.find_element(By.XPATH, '//picture[1]/img').get_attribute('src')
#         # print(image)
#     except:
#         image = ''
    
#     driver.get(brand_baseurl2.format(brand_slug))
#     instagram = ''
#     twitter = ''
#     facebook = ''
#     website = ''
#     other = ''
#     try:
#         social = driver.find_elements(By.CLASS_NAME, 'brand-social-links__SocialLink-sc-pohbyq-1')
#         for span in social:
#             if span.text == "Instagram":
#                 instagram = span.get_attribute('href')
#             elif span.text == "Twitter":
#                 twitter = span.get_attribute('href')
#             elif span.text == "Facebook":
#                 facebook = span.get_attribute('href')
#             elif span.text == "Website":
#                 website = span.get_attribute('href')
#             else:
#                 other = span.get_attribute('href')
#     except:
#         instagram = ''
#         twitter = ''
#         facebook = ''
#         website = ''
#         other = ''      
        
#     # section = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'section')))
#     row = [brand_names[count], facebook, instagram, twitter, website, other, details, license, image]
#     with open('brands_final.csv', 'a', encoding='utf-8', newline='') as f_object:
#         product_row = writer(f_object)
#         count = count + 1
#         if count == 1:
#             product_row.writerow(['Name', 'FaceBook', 'Instagram', 'Twitter','Website', 'Other', 'Details', 'License', 'ImageURL'])
#         product_row.writerow(row)
#         f_object.close()
