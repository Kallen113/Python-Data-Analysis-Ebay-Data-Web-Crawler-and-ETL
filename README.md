# Python-Data-Analysis-Ebay-Data-Web-Crawler-and-ETL
Python web crawler with Python+ SQL ETL of eBay data. Project will include Data visualizations and statistical, regression, or ML modeling where appropriate for analysis of eBay prices, etc.

I have added a working ebay_selenium_webcrawler_product_sale_price.py script that uses a diferent approach in data scraping. In this case, we are using selenium since it allows us to interact with elements of the frontend of a webpage, such as inputting keywords into a search form. 

More specifically, this script scrapes price, date sold, and various seller data pertaining to items that were recently sold on eBay. The script allows the user to input a keyword or set of keywords. A more specific set of keywords will provide more precise data since it will help narrow the resulting items to be closer to the items in which you want to have data. For more obscure items or very specific sets of keywords, the script will automatically filter out listings that do not match the keyword(s) if the number of matching listings is less than 60. The reason for this is that the default number of listings per page is 60.  

To-dos:
1) Consider adding an additional option in the ebay_selenium_webcrawler_product_sale_price.py script to allow users to select whether they want to only collect data on eBay listings that were sold via Auction or sold via a Buy it Now feature. Similarly, update the script to grab data on whether an item was sold via Buy it Now or Auction. 

2) Expand the project by doing a more detailed data analysis of some of the scraped data.

