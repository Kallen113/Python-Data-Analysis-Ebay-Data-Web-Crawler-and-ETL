""" For this webcrawler, we seek to scrape sale price data for a specific item, as specified by a given keyword.
The eBay advanced search form allows us to search for data pertaining to sold items specifically, so we 
should use this rather than the standard form.

The eBay advanced search form can be found at the following URL: <https://www.ebay.com/sch/ebayadvsearch>"""


def main():
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

    # use Chrome webdriver: specify options to help mitigate the chance of the webdriver missing HTML elements that we want to scrape and parse:
    options = Options()  # initialize Options() object, so we can customize and specify options for the web driver
    options.add_argument("--disable-extensions")  # disable any browser extensions
    options.add_argument("start-maximized")   # maximize webdriver's browser windows
    options.add_argument("disable-infobars") # disable browser infobars

    # import datetime module from date library so we can use today's date for outputted CSV file
    from datetime import date



    # install latest version of Chrome webdriver, via ChromeDriverManager
    web_driver  = webdriver.Chrome(
        # ChromeDriverManager().install(),  # install or update latest Chrome webdriver using using ChromeDriverManager() library
        # options=options  # implement the various options specified above
        )


    # specify URL for eBay's advanced search form--ie, the url for where we want to start the webcrawler
    url = 'https://www.ebay.com/sch/ebayadvsearch'

    # implement GET request to access url
    web_driver.get(url)



    ebay_product_name = input("Specify name of product you want to search for on eBay: ")

    # # get HTML element of the eBay search form
    # form_input = web_driver.find_elements_by_xpath('//*[@id="gh-ac"]')
    # form_input = web_driver.find_element(By.CLASS_NAME, 'textbox field_control textbox')
    # form_input = web_driver.find_element(By.CLASS_NAME, 'textbox__control')


    form_input = web_driver.find_element(By.ID, '_nkw')

    # type in the desired product name-- NB: selenium's send_keys() method allows you to submit data onto a form (ie, text)
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
    ))


    search_button.click()

    # initialize lists to contain prices, item names, condition (used vs new), date sold, and number of listing matches
    item_names = []

    item_prices = []

    condition = []

    date_sold = []

    seller_name = []

    matched_listings_count = []



    # scrape item names:
    # names = web_driver.WebDriverWait(web_driver, 39).until(EC.presence_of_element_located).find_elements(By.XPATH, "//div[@class='s-item__title']")

    # names = web_driver.find_elements(By.XPATH, "//h3[@class='s-item__title']")

    # names =  web_driver.find_elements(By.XPATH, "//span[@role='heading']")

    names = web_driver.find_elements(By.XPATH, "/html/body/div[5]/div[4]/div[2]/div[1]/div[2]/ul/li[3]/div/div[2]/a/div/span")



    # names = WebDriverWait(web_driver, 39).until(EC.presence_of_element_located(
    #     (By.XPATH, "/html/body/div[5]/div[4]/div[2]/div[1]/div[2]/ul/li[3]/div/div[2]/a/div/span")

    # ))

    # names = web_driver.find_elements(By.XPATH, "/html/body/div[5]/div[4]/div[2]/div[1]/div[2]/ul/li[3]/div/div[2]/a/div/span")


    #  = web_driver.find_elements(By.XPATH, "/html/body/div[5]/div[4]/div[2]/div[1]/div[2]/ul/li[3]/div/div[2]/a/div/span"
                                
    # iterate over each scraped element, and grab the text to get the data we actually need:

    for el in names:
        item_names.append(el.text)

    # scrape item prices
    prices = web_driver.find_elements(By.CLASS_NAME, "s-item__price")

    for el in prices:
        item_prices.append(el.text)


    # scrape item condition--ie, used vs new (etc) 
    item_condition = web_driver.find_elements(By.CLASS_NAME, 'SECONDARY_INFO')

    for el in item_condition:
        condition.append(el.text)


    # scrape date sold data
    # date_sold_listing = web_driver.find_elements(By.CLASS_NAME, 'POSITIVE')

    date_sold_listing = web_driver.find_elements(By.XPATH, "//div[@class='s-item__title--tag']")


        
    for el in date_sold_listing:
        date_sold.append(el.text)


    # scrape seller name (ie, user eBay user name of given seller)
    seller_name_scraped = web_driver.find_elements(By.XPATH, "//span[@class='s-item__seller-info-text']")

    for el in seller_name_scraped:
        seller_name.append(el.text)
        

    # scrape number of listings that match the search keyword(s)

    results_count_heading = web_driver.find_elements(By.XPATH, "//h1[@class='srp-controls__count-heading']")

    for results in results_count_heading:
        matched_listings_count.append(results.text)


    # clean matched_listings_count by grabbing only the number/counts of results text, instead of the entire "n results for {keyword}" text (ie, only keep the first--read 0th split()--word from the list)

    matched_listings_count = [el.split()[0] for el in matched_listings_count] # grab only the 0th substring, since this contains the results counts


    # sanity check
    # print(f"Item names:\n{item_names}")

    # print(f"Item prices:\n{item_prices}")

    print(f"len of Item names:\n{len(item_names)}")

    print(f"len of Item condition:\n{len(condition)}")

    print(f"len of date when Item was sold:\n{len(date_sold)}")

    print(f"matched_listings_count:\n{matched_listings_count}")

    # # data pipeline: transform the lists to a DataFrame. 
    # Transform the lists to a dictionary of lists, and then use .T to transpose the data so that we can include lists of varying length

    df = pd.DataFrame.from_dict(
        {'prices':item_prices,
        'item_names': item_names, 
        'condition': condition,
        'date_sold':date_sold,
        'seller_name':seller_name,
        'matched_listings_count':matched_listings_count
        },
        orient='index').T




    ## Data cleaning:

    # forward fill values of matched_listings_count so we do not delete it when removing null values for columns such as item_prices
    df['matched_listings_count'] = df['matched_listings_count'].ffill(axis=0)

    # remove dollar signs
    df['prices'] = df['prices'].str.replace('$', '')


    # extract only the first shown price, since some listings may have a range of price values (mapping the same product to multiple prices would overly complicate our data cleaning, data pipelines, and subsequent data analysis)
    df['prices'] = df['prices'].str.split().str.get(0)  # extract only the first price


    # transform prices to numeric, and specify downcast as float to use smallest needed float data type
    df['prices'] = pd.to_numeric(df['prices'], downcast='float')

    # remove any null prices or item condition rows
    df = df.dropna(subset=['prices', 'condition'])

    # sanity check
    print(f"Cleaned item prices:{df['prices']}")


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



    df['matched_listings_count'] = df['matched_listings_count'].str.replace(substr_pattern_replace_matched_count, '')

    # transform prices to numeric, and specify downcast as float to use smallest needed float data type
    df['matched_listings_count'] = pd.to_numeric(df['matched_listings_count'])

    # sanity check
    print(f"Listing date sold data:{df['date_sold']}")

    # ETL data pipeline df to CSV:
    # import datetime module from date library so we can use today's date for outputted CSV file
    from datetime import date
    import os

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

    df_to_CSV_data_pipeline(df, csv_prefix_name, ebay_product_name, path)


if __name__== "__main__":
    main()