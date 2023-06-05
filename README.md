# IKEA Product Web Scraper
This project focuses on the webscraping of IKEA products using Python, BeautifulSoup4, and Selenium. The key objective of this program is to gather information on IKEA's main product and their subproduct categories.

## Table of Contents
- [General Info](#general-info)
- [Technologies](#technologies)
- [Setup](#setup)
- [Usage](#usage)
- [Output Files](#output-files)
- [Contributing](#contributing)

## General Info
This project makes use of the powerful Python libraries BeautifulSoup4 and Selenium to scrape data from [IKEA Indonesia](https://www.ikea.co.id/in/produk). The primary aim is to collect information on IKEA products and their subcategories, including details like the product name, brand, color, dimensions, item ID, and price (in Indonesian Rupiah).

Selenium is used to access and download the HTML file from the IKEA website, while BeautifulSoup4 is utilized to parse, prettify and extract the required information from the HTML content. Specifically, BeautifulSoup4 is used to identify and capture the relevant `div` tags containing the required product details.

Running the program may take between 1-2 hours, depending on your internet connection.

## Technologies
Project is created with:
* Python 3.9
* BeautifulSoup4
* Selenium

## Setup
To run this project, install the necessary Python packages:

```
$ pip install beautifulsoup4
$ pip install selenium
```

You will also need to have the [correct WebDriver for your browser](https://www.selenium.dev/documentation/en/getting_started_with_webdriver/browsers/) installed.

## Usage
To run the script, navigate to the directory containing the project files and run:

```
$ python main.py
```

The script will then start collecting the data and save it into the specified files.

## Output Files
Upon successful execution of the program, the following files will be created in your working directory:

1. `dictvalues.csv` - Contains the category names, subcategories, and their respective URLs.
2. `seleniumhome.html` - The BeautifulSoup4 processed HTML file of the IKEA product home page.
3. `seleniumout.html` - BeautifulSoup4 processed HTML files of each URL found in `dictvalues.csv`.
4. `output.json` - A JSON file containing a list of dictionaries of each product. The dictionary values consist of name, brand, id item, price, color, dimension, variant, and category.
5. `ikea_products.csv` - The final output of the program, containing all the IKEA product information scraped from the website.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

---