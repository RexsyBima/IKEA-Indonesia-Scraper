from bs4 import BeautifulSoup
from selenium import webdriver
import json
import csv

def output(html_content):
    dict_category = {}
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
                

def scrape(html_content, data):
    datatempo = []
    with open('seleniumout.html', 'w') as file:
        """to write the html, BS, lxml it, then prettify it"""
        soup = BeautifulSoup(html_content, 'lxml')
        file.writelines(soup.prettify())
    

    with open('seleniumout.html', 'r') as file:
        """to read seleniumout.html, BS, lxml it, then prettify it, again... and also to search keywords"""
        content = file.read()
        soup = BeautifulSoup(content, 'lxml')
        item_cards = soup.find_all('input', {'name' : 'productInfo'})
#]        urls = soup.find_all('div', {'class': 'd-flex flex-row'}) 
        for itemcard in item_cards:
            value_str = itemcard['value']
            value_dict = json.loads(value_str)
            datatempo = data.append(value_dict)
#        for url in urls:
#            value_url = url.find('a')
#            href = value_url['href']
#            value_dict = json.loads(href)
#            datatempo = data.append(value_dict)
        return datatempo

def jsonsave(data):
    with open('output.json', 'w') as json_:
        """to write the data(var) containing list of dictionaries into a json"""
        json.dump(data, json_, indent=4)
            # This is the string representation of the JSON data you wanted.

def editdata(data):
    for data_ in data:
        name_parts = data_['name'].split(' - ')
        data_['brand'] = name_parts[0]
        descriptionparts = name_parts[1].split(', ')
        data_['product_name'] = descriptionparts[0]
        try:
            data_['color'] = descriptionparts[1]
        except IndexError:
            data_['color'] = "undefined"
        try:    
            data_['dimension'] = descriptionparts[2]
        except IndexError:
            data_['dimension'] = "undefined"
        del data_['name']
    return data

    # Define CSV file
def csvwrite(data):
    with open('ikea_products.csv', 'w', newline='') as csvfile:
        # Specify the field names
        fieldnames = ['product_name', 'brand', 'color', 'dimension', 'id', 'price', 'category', 'variant']

        # Create a writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write data rows
        for row in data:
            writer.writerow(row)