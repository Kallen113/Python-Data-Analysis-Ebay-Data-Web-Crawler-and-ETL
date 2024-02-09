""" For this webcrawler, we seek to scrape sale price data for a specific item, as specified by a given keyword.
The eBay advanced search form allows us to search for data pertaining to sold items specifically, so we 
should use this rather than the standard form.

The eBay advanced search form can be found at the following URL: <https://www.ebay.com/sch/ebayadvsearch>"""

# run webcrawler on each page until final page is reached
import random
import time

# import reduce module so we can flatten element from list, and convert to int in single line (ie, without explicit for loop)
from functools import reduce


import requests

import os

#web crawling, web scraping & webdriver libraries and modules
from selenium import webdriver  # NB: this is the main module we will use to implement the webcrawler and webscraping. A webdriver is an automated browser.
from webdriver_manager.chrome import ChromeDriverManager # import webdriver_manager package to automatically take care of any needed updates to Chrome webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options  # Options enables us to tell Selenium to open WebDriver browsers using maximized mode, and we can also disable any extensions or infobars

from click import option


# import webdriver_manager package to automatically take care of any needed updates to Chrome webdriver
from webdriver_manager.chrome import ChromeDriverManager 


import requests
import pandas as pd
import numpy as np


# import inquirer library so we can prompt user in command line to type in an item name for the web crawler to search for
import inquirer


# import inquirer library so we can prompt user in command line to type in an item name for the web crawler to search for
import inquirer 


## Define web-scraping functions for parsing either the xpath or class name of element for desired data:
def parse_html_via_xpath(web_driver, xpath_arg: str, list_to_append: list) -> list:
    """ Scrape data from HTML element by looking up xpath (via selenium's find_element("xpath") method), within a try except control flow clause to account for rental listings that are missing a given HTML element.
    a.) Except if a NoSuchElementException, TimeoutException, or if a WebDriverException occurs --indicating a given element does not exist or the WebDriver connection has been lost--add an 'nan' value indicating missing data.
    b.) If no exceptions are encountered, scrape (return) the HTML element and extract the element's text data."""
    try:
        # scrape the HTML element (if present), extract text, and append to given list
        scraped_html = web_driver.find_elements(By.XPATH, xpath_arg)

    except (NoSuchElementException) as e:
        """If the given rental listing page does not contain given element, append 'nan' value to indicate missing value."""
        return list_to_append.append('nan')  # indicate missing value
    
    # parse scraped data's text if no exception is encountered:
    for el in scraped_html:
        list_to_append.append(el.text)  # parse text data from scraped html element, and append to list for given variable of interest


def parse_html_via_class_name(web_driver, class_name_arg: str, list_to_append: list) -> list:
    """ Scrape data from HTML element by looking up xpath (via selenium's find_element("xpath") method), within a try except control flow clause to account for rental listings that are missing a given HTML element.
    a.) Except if a NoSuchElementException, TimeoutException, or if a WebDriverException occurs --indicating a given element does not exist or the WebDriver connection has been lost--add an 'nan' value indicating missing data.
    b.) If no exceptions are encountered, scrape (return) the HTML element and extract the element's text data."""
    try:
        # scrape the HTML element (if present), extract text, and append to given list
        scraped_html = web_driver.find_elements(By.CLASS_NAME, class_name_arg)

    except (NoSuchElementException) as e:
        """If the given rental listing page does not contain given element, append 'nan' value to indicate missing value."""
        return list_to_append.append('nan')  # indicate missing value
    
    # parse scraped data's text if no exception is encountered:
    for el in scraped_html:
        list_to_append.append(el.text)  # parse text data from scraped html element, and append to list for given variable of interest


def keep_first_n_matched_listings_count_if_only_single_page(scraped_data_list, matched_listings_count_int_el):
    # if matched_listings_count_int_el< 60, keep only the first n elements of scraped data list based on the value of the matched listings count 
    return scraped_data_list[0: matched_listings_count_int_el]


def scrape_data(web_driver, item_names, item_prices, condition, date_sold, seller_name, matched_listings_count, shipping_price, price_type):
    ## ensure we only grab the actual eBay listings data, and avoid extraneous price and other data existing above the listings data

    # this can be ensured by only grabbing data from the child elements within each eBay page's div element with class name of "srp-river-results clearfix"

    listings_data_ul_element = web_driver.find_element(By.XPATH, "//ul[@class='srp-results srp-list clearfix']")
    # listings_data_ul_element = parse_html_via_xpath("//ul[@class='srp-results srp-list clearfix']")


    ## Scrape the desired listings data--NB: only scrape from the listings_data_ul_element so that we are only scraping the actual listings data!

    # scrape item names, and append to list
    parse_html_via_xpath(web_driver, "//div[@class='s-item__title']", item_names)


    # data cleaning: remove extraneous item_names data, ie, with empty string
    item_names = [el for el in item_names if el] 


    # scrape item prices
    # prices = listings_data_ul_element.find_elements(By.CLASS_NAME, "s-item__price")

    # for el in prices:
    #     item_prices.append(el.text)

    # scrape item prices, and append to list
    parse_html_via_class_name(web_driver, "s-item__price", item_prices)


    # scrape item condition--ie, used vs new (etc) 
    # item_condition = listings_data_ul_element.find_elements(By.CLASS_NAME, 'SECONDARY_INFO')

    # for el in item_condition:
    #     condition.append(el.text)

    # scrape item condition, and append to list
    parse_html_via_class_name(web_driver, "SECONDARY_INFO", condition)


    # scrape date sold data
    # date_sold_listing = listings_data_ul_element.find_elements(By.CLASS_NAME, 'POSITIVE')

    # date_sold_listing = listings_data_ul_element.find_elements(By.XPATH, "//div[@class='s-item__title--tag']")


        
    # for el in date_sold_listing:
    #     date_sold.append(el.text)

    # parse item name
    parse_html_via_xpath(web_driver, "//div[@class='s-item__title--tag']", date_sold)


    # # parse bid count
    # parse_html_via_xpath(web_driver, "//span[@class='s-item__bids s-item__bidCount']", bids_count)

    # # scrape seller name (ie, user eBay user name of given seller)
    
    parse_html_via_xpath(web_driver, "//span[@class='s-item__seller-info-text']", seller_name)



    # # scrape number of listings that match the search keyword(s)

    parse_html_via_xpath(web_driver, "//h1[@class='srp-controls__count-heading']", matched_listings_count)



    # clean matched_listings_count by grabbing only the number/counts of results text, instead of the entire "n results for {keyword}" text (ie, only keep the first--read 0th split()--word from the list)

    matched_listings_count = [el.split()[0] for el in matched_listings_count] # grab only the 0th substring, since this contains the results counts

    # # scrape number of bids (NB: this would clearly be zero if a listing was sold via a Buy it Now option instead)
    # bids_count = listings_data_ul_element.find_elements(By.XPATH, "//span[@class='s-item__bids s-item__bidCount']")

    # for el in bids_count:
    #     bids_count.append(el.text)


    # # scrape shipping price
    # shipping_price_scraped = listings_data_ul_element.find_elements(By.XPATH, "//span[@class='s-item__shipping s-item__logisticsCost']")


    # for el in shipping_price_scraped:
    #     shipping_price.append(el.text)

    parse_html_via_xpath(web_driver, "//span[@class='s-item__shipping s-item__logisticsCost']", shipping_price)

    ## parse price type--ie, auction, buy it now, etc.
    # NB: auction is not explicitly denoted on eBay listings, instead we need to use a boolean "or" condition in which we check for number of bids (if any)
    # if the listing had 1 or more bids, then we can later use the number of bids for the bids_count list, and clean the price_type list such that we can specify replace the number of bids with "auction" for any such listing with bids!

    parse_html_via_xpath(web_driver, "//span[@class='s-item__purchase-options s-item__purchaseOptions' or @class='s-item__bids s-item__bidCount']",price_type)

    # parse_html_via_xpath(web_driver, "//div[@class='s-item__detail s-item__detail--primary']",price_type)
 

    # # sanity check
    # # print(f"Item names:\n{item_names}")

    # # print(f"Item prices:\n{item_prices}")

    # print(f"len of Item names:\n{len(item_names)}")

    # print(f"len of Item condition:\n{len(condition)}")

    # print(f"len of date when Item was sold:\n{len(date_sold)}")

    # print(f"matched_listings_count:\n{matched_listings_count}")


def main():


    # use Chrome webdriver: specify options to help mitigate the chance of the webdriver missing HTML elements that we want to scrape and parse:
    options = Options()  # initialize Options() object, so we can customize and specify options for the web driver
    options.add_argument("--disable-extensions")  # disable any browser extensions
    options.add_argument("start-maximized")   # maximize webdriver's browser windows
    options.add_argument("disable-infobars") # disable browser infobars

    # import datetime module from date library so we can use today's date for outputted CSV file
    from datetime import date

    # run webcrawler on each page until final page is reached
    import random
    import time

    # import reduce module so we can flatten element from list, and convert to int in single line (ie, without explicit for loop)
    from functools import reduce

    ## Install webdriver, get access to home page of advanced search, prompt user for search keywords, and type in search:

    # install latest version of Chrome webdriver, via ChromeDriverManager
    web_driver  = webdriver.Chrome(
        # ChromeDriverManager().install(),  # install or update latest Chrome webdriver using using ChromeDriverManager() library
        # options=options  # implement the various options specified above
        )


    # specify URL for eBay's advanced search form--ie, the url for where we want to start the webcrawler
    url = 'https://www.ebay.com/sch/ebayadvsearch'

    # implement GET request to access url
    web_driver.get(url)

    # minimize browser window for ease of user experience 
    web_driver.minimize_window()

    # prompt user for search keyword(s)
    ebay_product_name = input("Specify name of product you want to search for on eBay: ")

    # find element pertaining to the advanced search bar
    form_input = web_driver.find_element(By.ID, '_nkw')

    # type in the desired product name, as given by user prompt-- NB: selenium's send_keys() method allows you to submit data onto a form (ie, text)
    form_input.send_keys(ebay_product_name)

    # look for "Sold items" element, and wait until the element is clickable
    sold_items_clickable_element = WebDriverWait(web_driver, 39).until(EC.element_to_be_clickable(
        (By.XPATH, "//label[@for='s0-1-17-5[1]-[2]-LH_Sold']")
    )
        )


    # <label for="s0-1-17-5[1]-[2]-LH_Sold" class="field__label--end"><!--F#f_0[0]-->Sold items<!--F/--></label>

    # click "Sold items" so we filter the search to only consider items that have been sold on eBay:
    sold_items_clickable_element.click()

    # implement search by clicking "search" button
    search_button = WebDriverWait(web_driver, 39).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='btn btn--primary'][1]")
        )
        )

    # click search button to implement search of inputted keyword(s)
    search_button.click()

    ## initialize lists to contain all of the scraped data attributes: prices, item names, condition (used vs new), date sold, and number of listing matches
    item_names = []

    item_prices = []

    condition = []

    date_sold = []

    seller_name = []

    matched_listings_count = []

    # bids_count = []

    shipping_price= []

    # list to contain what pricing scheme was used for the sale--ie, buy it now, best offer, or auction (as denoted by having 1 or more bids)
    price_type = []

    # execute main webscraper scrape_data() function to scrape data, starting w/ first page of listings
    scrape_data(web_driver, item_names, item_prices, condition, date_sold, seller_name, matched_listings_count, shipping_price, price_type)


    # remove commas (if exists)--e.g., when number of listings is in thousands or higher
    matched_listings_count = [el.replace(",","") for el in matched_listings_count]

    # clean matched_listings_count so that we only retain the count of results, without the extraneous "results for {search keyword(s)...}"
    matched_listings_count = [el.split()[0] for el in matched_listings_count] # grab only the 0th substring, since this contains the results counts

    # remove plus sign (if exists)--ie, when number of listings is so high that eBay states n+ number of listings
    matched_listings_count = [el.rstrip("+") for el in matched_listings_count]

    print(f"Sanity check on matched listings count before converting to int:\n{matched_listings_count}")

    # Grab element of matched_listings_count as a single int object
    matched_listings_count_int_el = int(reduce(lambda s: s, matched_listings_count))

    ## Navigate to each next page if there are more than 60 listings matching the search keyword(s):

    # only click to next page if there are more matching listings on another page
    if matched_listings_count_int_el > 60: 

        # keep clicking onto next page of listings, if matching listings count exceeds 60
        while True:

            try:
                # specify xpath for the next page button (widget)
                next_page_button_xpath = "//a[@class='pagination__next icon-link']"       

                # wait up to 25 seconds to let HTML element load on given listing page
                wait_until = WebDriverWait(web_driver, 25)  
                next_page_element = wait_until.until(EC.visibility_of_element_located((By.XPATH, next_page_button_xpath)))                  

                next_page_element.click()

                # # keep clicking until the last page is reached, based on the next_page_element equaling 1 (ie, until it equals 0)
                # if (next_page_element != 0):  # verify the next page element still exists on given page, so next page can still be navigated to...
                #     next_page_element.click() # click next page element

                print("\nNavigating to the next page of eBay listings\n")

                # wait n seconds before accessing the next page, but randomize the amount of time delay, in order to mimic more human-like browser activity
                rand_sl_time = random.randrange(1, 4) # specify a range of pseudo-random values from 1 to 4 seconds
                time.sleep(rand_sl_time) # wait minimum of 1 second to let the page's various HTML contents to load, before we start extracting the various data on each subsequent page.
                print(f"\nURL of new page:\n{web_driver.current_url}\n\n")

                # scrape data on page, after clicking onto next page
                scrape_data(item_names, item_prices, condition, date_sold, seller_name, matched_listings_count, shipping_price)


            ## # ### scrape data

            # after next page button no longer exists, indicate final page has been reached                    
            # except (NoSuchElementException, ElementClickInterceptedException, TimeoutException) as e:
            except:
                # indicate that the last page has been reached
                print("\n**Last page reached**\n")

                # terminate the while true try..except loop, since all matching listings have been scraped
                break


    if matched_listings_count_int_el < 60: 
        # keep only scraped data records pertaining to search keywords by retaining only first n elements based on length of matched_listings_count_int_el
        item_names = keep_first_n_matched_listings_count_if_only_single_page(item_names, matched_listings_count_int_el)

        item_prices = keep_first_n_matched_listings_count_if_only_single_page(item_prices, matched_listings_count_int_el)
        condition = keep_first_n_matched_listings_count_if_only_single_page(condition, matched_listings_count_int_el)
        date_sold = keep_first_n_matched_listings_count_if_only_single_page(date_sold, matched_listings_count_int_el)
        seller_name = keep_first_n_matched_listings_count_if_only_single_page(seller_name, matched_listings_count_int_el)
        matched_listings_count = keep_first_n_matched_listings_count_if_only_single_page(matched_listings_count, matched_listings_count_int_el)
        shipping_price = keep_first_n_matched_listings_count_if_only_single_page(shipping_price, matched_listings_count_int_el)
        matched_listings_count = keep_first_n_matched_listings_count_if_only_single_page(matched_listings_count, matched_listings_count_int_el)
        # bids_count = keep_first_n_matched_listings_count_if_only_single_page(bids_count, matched_listings_count_int_el)

    # clean price_type by replacing substrings with more straight-forward labels
    price_type = [el.replace('or Best Offer', 'Buy it now') for el in price_type]

    price_type = [el.replace('Best offer accepted', 'Best Offer') for el in price_type]


    # additional data cleaning: ensure data are aligned correctly by removing extraneous empty strings () from 3 lists: item_prices, item_names, and condition-- NB: the extraneous data result from the xpath or class names being  scraped from top of webpage before any real listing's data start; there's no readily apparent method to avoid scraping these extranous data;

    # clean item prices data by removing extraneous empty string (ie, scraped from top of webpage before any real listings start)
    item_prices = [el for el in item_prices if el]

    # clean item_names data by removing extraneous empty string (ie, scraped from top of webpage before any real listings start)
    item_names = [el for el in item_names if el]

    # clean item condition data by removing extraneous empty string (ie, scraped from top of webpage before any real listings start)
    condition = [el for el in condition if el]

    # clean item price_type data by removing extraneous empty string (ie, scraped from top of webpage before any real listings start)
    price_type = [el for el in price_type if el]

    # parse number of bids data--NB: treat any non-bid listings as numpy nan values 
    # make a copy of price_type so we can parse the data without affecting the elements of the original price_type list
    bids_count  = list(price_type)

    for index, element in enumerate(bids_count[:]):
        if "bid" in element:
            
            bids_count[index] = element
        else:
            bids_count[index] = np.nan

    # clean price_type by classifying listings with bids as being an Auction
    for index, element in enumerate(price_type[:]):
        if "bid" in element:
            price_type[index] = 'Auction'
        else:
            price_type[index] = element

    # sanity check
    print(f"sanity check on price type (before cleaning bid count):\n {price_type}")

    # # data pipeline--transform the lists (columns) to a DataFrame. 
    # Transform the lists to a dictionary of lists, and then use .T to transpose the data so that we can include lists of varying length

    df = pd.DataFrame.from_dict(
        {'item_names': item_names,
        'price':item_prices, 
        'condition': condition,
        'date_sold':date_sold,
        'seller_name':seller_name,
        'matched_listings_count':matched_listings_count,
        'bids_count':bids_count,
        'shipping_price':shipping_price,
        'price_type':price_type
        },
        orient='index').T

    ## Data cleaning:

    # assign the value of the first row to the entire 'matched_listings_count' col (since this first row contains the accurate listings count value)
    df['matched_listings_count'] = df['matched_listings_count'][0]


    # replace empty strings with explicit numpy null ('NaN') values:
    df[['item_names', 'price']] = df[['item_names', 'price']].replace('', np.nan)

    print(f"Sanity check after replacing empty strings with null values:/n{df}")

    # # # clean matched_listings_count by grabbing only the number/counts of results text, instead of the entire "n results for {keyword}" text (ie, only keep the first--read 0th split()--word from the list)
    # # matched_listings_count = [el.split()[0] for el in matched_listings_count] # grab only the 0th substring, since this contains the results counts

    # df['matched_listings_count'] = df['matched_listings_count'].str.split()[0] # grab only the 0th substring, since this contains the results counts

    # # forward fill values of matched_listings_count so we do not delete it when removing null values for columns such as item_prices
    # df['matched_listings_count'] = df['matched_listings_count'].ffill(axis=0)


    # clean prices data: remove "$" signs and any commas  
    # # specify pattern of substrings we want to delete from the prices data, and join to pipe symbol (ie, OR Boolean in the Pandas library)
    # substr_pattern_replace_prices =  '|'.join([',', '$'])

    # df['price'] = df['price'].str.replace(substr_pattern_replace_prices, '')

    # specify pattern of substrings we want to delete from the prices data, and join to pipe symbol (ie, OR Boolean in the Pandas library)
    substr_pattern_replace_prices =  '|'.join([',', '$'])

    df['price'] = df['price'].str.replace('$', '')
    df['price'] = df['price'].str.replace(',', '')


    # extract only the first shown price, since some listings may have a range of price values (mapping the same product to multiple prices would overly complicate our data cleaning, data pipelines, and subsequent data analysis)
    df['price'] = df['price'].str.split().str.get(0)  # extract only the first price


    # transform prices to numeric, and specify downcast as float to use smallest needed float data type
    # df['price'] = pd.to_numeric(df['price'], downcast='float')

    # df['price'] = pd.to_numeric(df['price'], downcast='float')

    df['price']  = pd.to_numeric(df.price, 'coerce').round(2).fillna(df.price)


    # remove any null prices or item condition rows
    df = df.dropna(subset=['price', 'condition'])

    # sanity check
    print(f"Cleaned item prices:{df['price']}")


    # clean seller name data: the scraped data actually includes 3 substring elements related to sellers: a) the seller username; b) number of seller's ratings, & c) % of positive feedback for seller

    # extract the number of seller ratings by grabbing only the 2nd substring word from the seller_name col 
    df['seller_ratings_count'] = df['seller_name'].str.split().str.get(1)

    # remove commas
    df['seller_ratings_count'] = df['seller_ratings_count'].str.replace(',', '')

    # remove parantheses
    df['seller_ratings_count'] = df['seller_ratings_count'].str.replace(r"\(|\)", "")


    # extract the % of positive feedback ratings by grabbing only the 3rd substring word from the seller_name col 
    df['perc_positive_feedback'] = df['seller_name'].str.split().str.get(2)


    # remove percent signs
    df['perc_positive_feedback'] = df['perc_positive_feedback'].str.replace('%', '')

    # grab the seller name by itself
    df['seller_name'] = df['seller_name'].str.split().str.get(0)

    # remove extraneous "Sold " & "\nSold" Item substrings from date_sold col:

    # specify pattern of substrings we want to delete, and join to pipe symbol (ie, the OR Boolean in the Pandas library)
    substr_pattern_replace_date_sold =  '|'.join(['Sold', '\nSold Item'])

    df['date_sold'] = df['date_sold'].str.replace(substr_pattern_replace_date_sold, '')


    # remove "," or "+" symbols if either exist
    # specify pattern of substrings we want to delete, and join to pipe symbol (ie, OR Boolean in the Pandas library)
    substr_pattern_replace_matched_count =  '|'.join([',', '\+'])

    df['matched_listings_count'] = df['matched_listings_count'].str.replace(substr_pattern_replace_matched_count, '', regex=True)

    # transform matched listings count to numeric, and specify downcast as float to use smallest needed float data type
    df['matched_listings_count'] = pd.to_numeric(df['matched_listings_count'])

    # clean bids_count by removing any 'bids' or 'bid' substrings
    substr_pattern_bid =  '|'.join(['bid', 'bids'])

    df['bids_count'] = df['bids_count'].str.replace(substr_pattern_bid, "", regex=False)


    ## clean shipping_price data:

    # Specify records with "Free shipping" substr so we can consistently convert the column to numeric 
    df['shipping_price'] = df['shipping_price'].str.replace("Free shipping", "0")

    # remove plus sign, dollar sign, and "shipping" substrings from col, again so we can convert it to numeric
    # substr_pattern_replace_shipping_price =  '|'.join(['\+', '$', 'shipping']) # specify the list of all 3 substrings we want to delete from col, and use '|' OR boolean operator

    # df['shipping_price'] = df['shipping_price'].str.replace(substr_pattern_replace_shipping_price, '')

    # remove plus sign
    df['shipping_price'] = df['shipping_price'].str.replace('\+', '')

    # remove dollar sign
    df['shipping_price'] = df['shipping_price'].str.replace('$', '')

    # remove 'shipping' substr
    df['shipping_price'] = df['shipping_price'].str.replace('shipping', '')

    # remove 'estimate' substr
    df['shipping_price'] = df['shipping_price'].str.replace('estimate', '')

    # account for possibility of certain shipping prices to be unkown based on listing not having specified a shipping price
    df['shipping_price'] = df['shipping_price'].str.replace('Shipping not specified', '')  # delete aby unspecified shipping prices since we cannot verify shipping price in these instances

    # sanity check
    print(f"Initial cleaning of shipping prices (still str):{df['shipping_price']}")

    # remove any columns with missing shipping price data (ie, literally empty strings '' given shipping_price is still an object column)
    df = df[df['shipping_price']!='']

    # transform shipping_price col to numeric
    df['shipping_price']  = pd.to_numeric(df.shipping_price, 'coerce').round(2).fillna(df.shipping_price)

    # sanity check
    print(f"Final data cleaning and transformation of shipping prices to numeric:{df['shipping_price']}")
    
    # compute total price by adding the base price with the shipping price, as new col
    df['total_price'] = df['price'] + df['shipping_price']

    # remove any shipping_price nulls
    df = df.dropna(subset=['shipping_price'])


    # to ensure we are only looking at listings that definitely contain the search keyword, filter the data to only the matching keyword matches if the number of keyword matches is less than 60 (ie, less than the 1st full page of listings):
    if df['matched_listings_count'].iloc[0] < 60:  # ie, check if the number of listings matching the search keyword(s) is less than 60
        df = df.head(df['matched_listings_count'].iloc[0])  # filter data if eBay has tacked on the listings page with related listings that do *not* contain the search keyword
        
    else:
        pass

    # sanity check
    print(f"Listing date sold data:{df['date_sold']}")

    # ETL data pipeline df to CSV:


    # get today's date to use for CSV file name
    def df_to_CSV_data_pipeline(df, csv_prefix_name, ebay_product_name, path):
        ## specify CSV file name, but first get today's date:

        # get today's date as str
        date_today_str = str(date.today())
        # specify underscore -- ie, '_' --as file name separator using f-strings
        underscore_separator = '_'
        # CSV file extension
        csv_ext = '.csv'

        ## specify full CSV file name using f string:
        # include the search keyword and today's date as parts of the CSV file name
        csv_file_name = f'{csv_prefix_name}{underscore_separator}{ebay_product_name}{underscore_separator}{date_today_str}{csv_ext}'

        # use os.join() soo we can save the file to specified path
        return df.to_csv(os.path.join(path, csv_file_name), index=False) # do not save index

    # specify path to save ebay price data
    path = r'D:\Coding and Code projects\Python\ebay_data_proj\ebay_price_data'

    csv_prefix_name = 'ebay_price_data'

    # final data cleaning before executing to_csv pipeline:

    # remove any symbols that are not permitted as CSV file names from ebay_product_name
    forbidden_csv_file_name_symbols = [':', '<', '>', '*', '|', '/', '[', ']', '"']

    # iterate over each specified symbol we want to remove from ebay_product_name (if applicable)
    for string in forbidden_csv_file_name_symbols:
            ebay_product_name = ebay_product_name.replace(string, '') # remove undesired symbols and chars


    df_to_CSV_data_pipeline(df, csv_prefix_name, ebay_product_name, path)

if __name__== "__main__":
    main()
