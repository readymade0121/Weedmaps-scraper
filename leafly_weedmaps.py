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


#the script for weedmap strain

strain_origin_url = "https://api-g.weedmaps.com/wm/v1/strains?"
strain_page_per_take = 100  # 18
strain_page_num = 15

strainList_slug = []
strainList_name = []
strainList_url = []
strainList_category = []
strainList_thc = []
strainList_cbd = []
strainList_effects = []
strainList_desc = []
strainList_flavors = []
# strainList_helpwith = []
ua = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': 'PostmanRuntime/7.26.8', 'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive'}


def scrapStrains():

    for x in range(strain_page_num):
        strain_get_url = (
            strain_origin_url + "&page={}&page_size={}").format(x+1, strain_page_per_take)
        response = requests.get(strain_get_url, headers=headers)
        strains = json.loads(response.text)['data']
        for y in strains:
            strainList_slug.append(y['attributes']['slug'])
            strainList_name.append(y['attributes']['name'])
            strainList_url.append(y['attributes']['hero_image_url'])
            strainList_category.append(y['attributes']['species'])
            strainList_thc.append(y['attributes']['thc_max'])
            strainList_cbd.append(y['attributes']['cbd_max'])
            strainList_desc.append(y['attributes']['description'])

            _ef = ''
            for z in y['attributes']['effects']:
                _ef += z['name'] + ','
            strainList_effects.append(_ef)
            _fl = ''
            for z in y['attributes']['flavors']:
                _fl += z['name'] + ','
            strainList_flavors.append(_fl)

scrapStrains()
df = pd.DataFrame({
    'name': strainList_name,
    'url': strainList_url,
    'category': strainList_category,
    'thc': strainList_thc,
    'cbd': strainList_cbd,

    'Top effect': strainList_effects,
    'description': strainList_desc,
    'flavors': strainList_flavors,

})
df.to_excel('weedstrains.xlsx', index=False, encoding='utf-8')

print("strain_weedmap_done")

#the script for leafly strain

strain_origin_url = "https://consumer-api.leafly.com/api/strain_playlists/v2?"
strain_page_per_take = 18  # 18
strain_page_num = 341

strainList_slug = []
strainList_name = []
strainList_url = []
strainList_category = []
strainList_thc = []
strainList_cbd = []
strainList_rating = []
strainList_flavor_aroms = []
strainList_topeffect = []
strainList_desc = []
strainList_feelings = []
strainList_negatives = []
strainList_flavors = []
strainList_helpwith = []

option = Options()
option.headless = True
driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.maximize_window()

def scrapStrains():

    for x in range(strain_page_num):
        strain_get_url = strain_origin_url + "&skip={}&take={}"
        response = requests.get(strain_get_url.format(x+1, strain_page_per_take))
        strains = json.loads(response.text)['hits']['strain']
        for y in strains:
            strainList_slug.append(y['slug'])
            strainList_name.append(y['name'])
            strainList_url.append(y['nugImage'])
            strainList_category.append(y['category'])
            strainList_thc.append(
                y['cannabinoids']['thc']['percentile50'])
            strainList_cbd.append(
                y['cannabinoids']['cbd']['percentile50'])
            strainList_rating.append(y['averageRating'])


def scrapStrainDetail(url):
    driver.get(url)
    try:
        strainList_flavor_aroms.append(driver.find_element(
            By.XPATH, "//section[1]/div/div[2]/div/div[4]/div/a/div/span[2]").text)
    except:
        strainList_flavor_aroms.append('')
    try:
        strainList_topeffect.append(driver.find_element(
            By.XPATH, "//section[1]/div/div[2]/div/div[4]/div[2]/a/div/span[2]").text)
    except:
        strainList_topeffect.append('')
    try:
        strainList_desc.append(driver.find_element(
            By.XPATH, "//section[1]/div/div[2]/div[2]/div/div").text)
    except:
        strainList_desc.append('')
    try:
        strainList_feelings.append(
            driver.find_element(By.XPATH, "//section[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div[1]/a/p").text+"," +
            driver.find_element(By.XPATH, "//section[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div[2]/a/p").text+"," +
            driver.find_element(
                By.XPATH, "//section[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div[3]/a/p").text
            )
    except:
        strainList_feelings.append('')
    try:
        strainList_negatives.append(
            driver.find_element(By.XPATH, "//section[2]/div[2]/div/div[2]/div/div/div/div[3]/div/div/div[1]/a/p").text+"," +
            driver.find_element(By.XPATH, "//section[2]/div[2]/div/div[2]/div/div/div/div[3]/div/div/div[2]/a/p").text+"," +
            driver.find_element(
                By.XPATH, "//section[2]/div[2]/div/div[2]/div/div/div/div[3]/div/div/div[3]/a/p").text
            )
    except:
        strainList_negatives.append('')
    try:
        strainList_flavors.append(
            driver.find_element(By.XPATH, "//section[2]/div[2]/div/div[2]/div/div[2]/div/div[1]/a/p").text+"," +
            driver.find_element(By.XPATH, "//section[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/a/p").text+"," +
            driver.find_element(
                By.XPATH, "//section[2]/div[2]/div/div[2]/div/div[2]/div/div[3]/a/p").text
            )
    except:
        strainList_flavors.append('')
    try:
        strainList_helpwith.append(driver.find_element(
            By.XPATH, "//section[2]/div[2]/div/div[2]/div[2]/ul").text)
    except:
        strainList_helpwith.append('')

scrapStrains()

for si in strainList_slug:
    st_url = "https://www.leafly.com/strains/" + si
    scrapStrainDetail(st_url)

df = pd.DataFrame({
        'name' : strainList_name,
        'url':strainList_url,
        'category':strainList_category,
        'thc':strainList_thc,
        'cbd':strainList_cbd,
        'rating':strainList_rating,
        'flavor&aroms':strainList_flavor_aroms,
        'Top effect':strainList_topeffect,
        'description':strainList_desc,
        'feelings':strainList_feelings,
        'negatives':strainList_negatives,
        'flavors':strainList_flavors,
        'help with':strainList_helpwith
    })
df.to_csv('strain_leafly.csv')

print("strain_leafly_done")

#the script for products of leafly.

driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.maximize_window()
indica_url="https://www.leafly.com/products/collections/indica?page={}"
sativa_url="https://www.leafly.com/products/collections/sativa?page={}"

indica_page_num=1  #534
indica_page_per_take=1  #18

sativa_page_num=0 #411
sativa_page_per_take=1

productList_slug=[]

for x in range(indica_page_num):
    url=indica_url.format(x+1)
    driver.get(url)
    for y in range(indica_page_per_take):
        # print(y)
        try:
            if(y<8): 
                productList_slug.append(driver.find_element(By.XPATH, "/html/body/main/div[2]/div[2]/div[2]/div[2]/div[3]/section[1]/div[{}]/article/a".format(y+1)).get_attribute("href"))
            elif(y>=8 and y<12): 
                productList_slug.append(driver.find_element(By.XPATH, "/html/body/main/div[2]/div[2]/div[2]/div[2]/div[3]/section[1]/div[{}]/article/a".format(y+2)).get_attribute("href"))
            elif(y>=12): 
                productList_slug.append(driver.find_element(By.XPATH, "/html/body/main/div[2]/div[2]/div[2]/div[2]/div[3]/section[1]/div[{}]/article/a".format(y+3)).get_attribute("href"))
        except:
            continue
for x in range(sativa_page_num):
    url=sativa_url.format(x+1)
    driver.get(url)
    for y in range(sativa_page_per_take):
        try:
            if(y<8): 
                productList_slug.append(driver.find_element(By.XPATH, "/html/body/main/div[2]/div[2]/div[2]/div[2]/div[3]/section[1]/div[{}]/article/a".format(y+1)).get_attribute("href"))
            elif(y>=8 and y<12): 
                productList_slug.append(driver.find_element(By.XPATH, "/html/body/main/div[2]/div[2]/div[2]/div[2]/div[3]/section[1]/div[{}]/article/a".format(y+2)).get_attribute("href"))
            elif(y>=12): 
                productList_slug.append(driver.find_element(By.XPATH, "/html/body/main/div[2]/div[2]/div[2]/div[2]/div[3]/section[1]/div[{}]/article/a".format(y+3)).get_attribute("href"))
        except:
            continue
productList_name=[]
productList_url=[]
productList_strain_name=[]
productList_kind=[]
productList_thc=[]
productList_cbd=[]
productList_rating=[]
productList_strain_rating=[]
productList_desc=[]
productList_strain_desc=[]
productList_feelings=[]
productList_negatives=[]
productList_helpwith=[]
productList_brand_name=[]
productList_brand_url=[]
productList_brand_desc=[]

for pi in productList_slug:
    driver.get(pi)
    try:
        productList_name=driver.find_element(By.XPATH, "/html/body/div/div[15]/main/div[1]/div[2]/div[2]/div/div[1]/h1").text
    except:
        productList_name.append('')
    try:
        productList_url=driver.find_element(By.XPATH, '/html/body/div/div[15]/main/div[1]/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div/ul/li[1]/div/div/picture/source[1]').get_attribute('srcset')
    except:
        productList_url.append('')
    try:
        productList_strain_name=driver.find_element(By.XPATH, '/html/body/div/div[15]/main/div[1]/div[2]/div[4]/div/div[1]/div[1]/div/div[2]/a').text
    except:
        productList_strain_name.append('')   
    try:
        productList_kind=driver.find_element(By.XPATH, '/html/body/div/div[15]/main/div[1]/div[2]/div[2]/div/div[1]/div[2]/div[1]/span[1]').text
    except:
        productList_kind.append('')
    try:
        productList_thc=driver.find_element(By.XPATH, '/html/body/div/div[15]/main/div[1]/div[2]/div[2]/div/div[1]/div[2]/div[1]/span[2]').text
    except:
        productList_thc.append('')
    try:
        productList_cbd=driver.find_element(By.XPATH, '/html/body/div/div[15]/main/div[1]/div[2]/div[2]/div/div[1]/div[2]/div[1]/span[3]').text
    except:
        productList_cbd.append('')
    try:
        productList_rating=driver.find_element(By.XPATH, '//div[@class="mb-xs"]//span[@class="pr-xs"]').text

    except:
        productList_rating.append('')
    try:
        productList_strain_rating=driver.find_element(By.XPATH, '//div[@class="mb-sm"]//span[@class="pr-xs"]').text
        
    except:
        productList_strain_rating.append('')
    try:
        productList_desc=driver.find_element(By.XPATH, '/html/body/div/div[15]/main/div[1]/div[2]/div[3]/div/div/div/div/div/div').text
    except:
        productList_desc.append('')
    try:
        productList_strain_desc=driver.find_element(By.XPATH, '//div[@class="mb-xxl"]//p').text
    except:
        productList_strain_desc.append('')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    try: 
        productList_feelings = soup.find(
                'div', {'class': 'react-tabs-padding'}).find_next({'div'}).find_next({'div'}).find_all({'div'})[1]
        productList_feelings = productList_feelings.text
        
    except Exception as E:
        print('err', E)
        productList_feelings.append('')
    try:    
        productList_negatives = soup.find(
                'div', {'class': 'react-tabs-padding'}).find_all({'div'})[16]
        productList_negatives = productList_negatives.text
    except:
        productList_negatives.append('')
    try: 
        productList_helpwith = soup.find(
                'div', {'class': 'react-tabs-padding'}).find_all({'div'})[29]
        productList_helpwith = productList_helpwith.text
    except:
        productList_helpwith.append('')
    try:
        productList_brand_desc = soup.find('div', {'data-testid': 'about-brand' }).find_next({'div'}).find_next({'div'}).find_next({'div'}).find_all({'div'})[3]
        productList_brand_desc=productList_brand_desc.text
    except Exception as E:
        print('err', E)
        productList_brand_desc.append('')
    try:
        productList_brand_name = soup.find('div', {'data-testid': 'about-brand' }).find_next({'div'}).find_all({'div'})[9]
        productList_brand_name=productList_brand_name.text
    except Exception as E:
        print('err', E)
        productList_brand_name.append('')
    try:    
        productList_brand_url=soup.find('div', {'data-testid': 'about-brand' }).find_all({'img'})
        productList_brand_url=productList_brand_url[0].get('data-srcset')
    except Exception as E:
        print('err', E)
        productList_brand_url.append('')
    
    row = [productList_name, productList_url, productList_strain_name, productList_kind, productList_thc, productList_cbd, productList_rating,
        productList_strain_rating, productList_desc, productList_strain_desc, productList_feelings, productList_negatives,
        productList_helpwith,
        productList_brand_name,
        productList_brand_url,
        productList_brand_desc]
    # print(row)
    with open('[product_leafly.csv', 'a', encoding='utf-8', newline='') as f_object:
 
        product_row = writer(f_object)
 
        product_row.writerow(row)
 
        f_object.close()