# Python-Data-Analysis-Ebay-Data-Web-Crawler-and-ETL
Python web crawler with Python+ SQL ETL of eBay data. Project will include Data visualizations and statistical, regression, or ML modeling where appropriate for analysis of eBay prices, etc.

I have added a working ebay_selenium_webcrawler_product_sale_price.py script that uses a diferent approach in data scraping. In this case, we are using selenium since it allows us to interact with elements of the frontend of a webpage, such as inputting keywords into a search form. 

More specifically, this script scrapes price, date sold, and various seller data pertaining to items that were recently sold on eBay. The script allows the user to input a keyword or set of keywords. A more specific set of keywords will provide more precise data since it will help narrow the resulting items to be closer to the items in which you want to have data. For more obscure items or very specific sets of keywords, the script will automatically filter out listings that do not match the keyword(s) if the number of matching listings is less than 60. The reason for this is that the default number of listings per page is 60.  

To-dos:
1) Expand the ebay_selenium_webcrawler_product_sale_price.py script to iterate over multiple pages of listings, for keyword searches in which there are more than 60 matched results (ie, greater than the default number of listings per page).

2) The product names are not being scraped properly (no errors are shown when running the script, but no data are beng scraped either), even though the Xpath argument seems to be correct. Try a different approach to help identify and scrape the correct data.

3) Expand the project by doing a more detailed data analysis of some of the scraped data.
