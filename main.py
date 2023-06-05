#please pip install -r requirements.txt to venv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options

import csv
import functions

data = []
dict_category = {}

"""to get and read the html page"""
driver = webdriver.Edge('/usr/local/bin/msedgedriver') #locate the browser bot for Edge
driver.set_page_load_timeout(200)
options = Options()
options.headless = True 
driver.implicitly_wait(60)

driver.get("https://www.ikea.co.id/in/produk") #launch the browser bot to the url
html_content = driver.page_source #get url html file
functions.output(html_content=html_content) #extract important/target main category, subcategories, and urls inside html, then store it to dictvalues.csv

with open('dictvalues.csv', 'r') as file: #read dictvalues
    reader = csv.DictReader(file)
    for row in reader:
        url = row['URL']
        page = 1
        while True:
            fix_url = f"https://{url}?sort=RECOMMENDED&page={str(page)}" #repetition for every url and pages until they returned empty None value
            driver.get(fix_url)
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'lxml')
            content = soup.find_all('input', {'name' : 'productInfo'})
            page += 1
            functions.scrape(html_content=html_content, data = data) #scrape to seleniumout.html (a temp html file), then append the target values to data List (which btw contains List of Dictionaries)
            if not content: #if value return None or empty, it will break and continue to the next lines of codes 
                break
    
    
functions.jsonsave(data=data) #to write the data(var) containing list of dictionaries into a json
functions.editdata(data=data) #to edit each List of data variabel, to a form of dictionary. ex = {'name' : 'productnamexyz', 'brand' : 'brandnamexyz'...color..dimension} 
functions.csvwrite(data=data) #to write into ikea_products.csv

driver.quit()
print("done")
    

"""
this code below is useless and for educational only
"""
    # If you want to convert the string to an actual dictionary (Python's version of a JSON object),
    # you can use json.loads:
#    value_dict = json.loads(value_str)
    # This is the dictionary representation of the JSON data. 
#    print(value_dict)
    
#Todo=get rid of it above


#with open('output.json', 'w') as output:
#    """to write into output.json file (for testing)"""
#    for name in item_cards:
#        output.writelines(str(name.input) + '\n')
#
#
## First, read the HTML file
#with open('output.html', 'r') as file:
#    html_content = file.read()
#
## Parse it with Beautiful Soup
#soup = BeautifulSoup(html_content, 'html.parser')
#
## Find all the input elements
#
#input_elements = soup.find_all('input', {'name': 'productInfo'}) 
#
#
## For each input element, extract its value and parse it as JSON
#with open('output.json', 'w') as file:
#    for input_element in input_elements:
#        value_str = input_element['value']
#        value_dict = json.loads(value_str)
#        json.dump(value_dict, file, indent=4)


"""
THIS CODE BELOW IS USELESS AND TO USE FOR EDUCATION ONLY
"""    
    # or do whatever you want with the dict

# For each input element, extract its value and parse it as a dictionar

#URL = 'https://www.ikea.co.id/in/produk/lemari/lemari-pakaian-modular'
#
#def scrape(url):
#    """to scrape a page source from url"""
#    response = requests.get(url)
#    source = response.text
#    return source
# 
#with open('coba.html', 'w') as coba_file:
#    """save the scraped page source into coba.html"""
#    coba_file = coba_file.writelines(scrape(url=URL))
#
#with open('cobaprettify.html', 'r+') as home_file:
#    """prettify coba.html"""
#    content = home_file.read()
#    soup = BeautifulSoup(content, 'lxml')
#    home_file.writelines(soup.prettify())
#    
#    ikea_html_tags = soup.find_all('h6')
#    for ikea in ikea_html_tags:
#        print(ikea.text)
 
    
