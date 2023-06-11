#please pip install -r requirements.txt to venv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import csv
import json

data = []
dict_category = {}
datatempo = []
urllist = []

"""to get and read the html page"""
driver = webdriver.Edge('/usr/local/bin/msedgedriver') #locate the browser bot for Edge
driver.set_page_load_timeout(200)
driver.implicitly_wait(120)

driver.get("https://www.ikea.co.id/in/produk") #launch the browser bot to the url
html_content = driver.page_source #get url html file
with open('seleniumhome.html', 'w') as file:
    """to write the html, BS, lxml it, then prettify it"""
    soup = BeautifulSoup(html_content, 'lxml')
    file.writelines(soup.prettify())
with open('seleniumhome.html', 'r') as file:
    """to read seleniumhome.html, BS, lxml it, then prettify it, again... and also to search keywords"""
    content = file.read()
    soup = BeautifulSoup(content, 'lxml')
    divs = soup.find_all("div", {"class": "col-sm-6 col-md-3 col-lg-3 text-left"})
    for div in divs:
        # Get the h2 text for the key of the dictionary
        key = div.find("h2").get_text(strip=True)
        # Find all a tags within this div and create a dictionary with text as key and href as value
        values = [{"name": a.get_text(strip=True), "url": "www.ikea.co.id" + a.get("href")} for a in div.find_all("a")]
        # Append to the dictionary
        dict_category[key] = values
# Create a writer object
with open('dictvalues.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Category", "Name", "URL"])
    for category, subcategories in dict_category.items():
        for subcategory in subcategories:
            writer.writerow([category, subcategory['name'], subcategory['url']])

WebDriverWait(driver, 30)

with open('dictvalues.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        url = row['URL']
        page = 1
        while True:
            fix_url = f"https://{url}?sort=RECOMMENDED&page={str(page)}"
            print(fix_url)
            driver.get(fix_url)
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'lxml')
            test = soup.find_all('input', {'name' : 'productInfo'})
            print(test)
            if not test:
                break
            page += 1
            with open('seleniumout.html', 'w') as file:
                """to write the html, BS, lxml it, then prettify it"""
                soup = BeautifulSoup(html_content, 'lxml')
                file.writelines(soup.prettify())
            with open('seleniumout.html', 'r') as file:
                """to read seleniumout.html, BS, lxml it, then prettify it, again... and also to search keywords"""
                content = file.read()
                soup = BeautifulSoup(content, 'lxml')
                item_cards = soup.find_all('input', {'name' : 'productInfo'})
                for itemcard in item_cards:
                    value_str = itemcard['value']
                    value_dict = json.loads(value_str)
                    data.append(value_dict)
            with open('seleniumout.html', 'r') as file:
                """to read seleniumout.html, BS, lxml it, then prettify it, again... and also to search keywords"""
                content = file.read()
                soup = BeautifulSoup(content, 'lxml')
                item_urls = soup.find_all('div', class_= 'd-flex flex-row') 
                for item_url in item_urls:
                    urlfix = item_url.find('a')
                    href = f"https://www.ikea.co.id{urlfix.get('href') if url else None}"
                    urllist.append(href)
                for item, urlfix in zip(data, urllist):
                    item['url'] = urlfix   

for data_ in data:
    name_parts = data_['name'].split(' - ')
    data_['brand'] = name_parts[0]
    descriptionparts = name_parts[1].split(', ')
    data_['product_name'] = descriptionparts[0]
    try:
        if "cm" in descriptionparts[1]:
            data_['color'] = 'undefined'
        elif "cm" not in descriptionparts[1]:
            data_['color'] = descriptionparts[1]
    except IndexError:
        data_['color'] = "undefined"
    try:
        if "cm" in descriptionparts[1]:
            data_['dimension'] = descriptionparts[1]
        else:
            data_['dimension'] = descriptionparts[2]
    except IndexError:
        data_['dimension'] = "undefined"
    del data_['name']
    
with open('output.json', 'w') as json_:
    """to write the data(var) containing list of dictionaries into a json"""
    json.dump(data, json_, indent=4)


with open('ikea_products.csv', 'w', newline='') as csvfile:
    # Specify the field names
    fieldnames = ['product_name', 'brand', 'color', 'dimension', 'id', 'price', 'category', 'variant', 'url']
    # Create a writer object
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # Write the header row
    writer.writeheader()
    # Write data rows
    for row in data:
        writer.writerow(row)
#print(data)
#print(type(data))
#print(urllist)
