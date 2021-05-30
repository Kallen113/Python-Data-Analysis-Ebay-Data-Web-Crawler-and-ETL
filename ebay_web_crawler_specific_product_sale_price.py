import requests
import csv
import scrapy

"""This web crawler will extract price, item description,
and sale data
from a specific eBay product, as denoted by a specific keyword.

NB: check the following GitHub repo, where I will store this script and all other
files, folders, etc. pertaining to this project:
<https://github.com/Kallen113/Python-Data-Analysis-Ebay-Data-Web-Crawler-and-ETL.git>

The GitHub repo is named as follows:
"Python-Data Analysis-Ebay Data Web Crawler  and ETL".

While the BeautifulSoup library could be feasible, we will 
INSTEAD use the scrapy framework, as it gives us more flexibility and power for extracting 
and downloading data, which is more in line with the goals of this web scraper.

The following YT video comprises a tutorial on how to do this:
<https://www.youtube.com/watch?v=csj1RoLTMIA&ab_channel=JohnWatsonRooney>

Also see this YT video for a more detailed web scraper 
for ebay data:
<https://www.youtube.com/watch?v=FLPYdzj8wYk&ab_channel=BetaHex>

In addition, here's scrapy documentation on the Spiders classes, which will 
perform a crawl via a provided URL link and extrct specific items from the URL page:
<https://docs.scrapy.org/en/latest/topics/spiders.html>

Finally, for a detailed web app ebay scraping python project, 
see the main web scraper script as follows:
<https://github.com/cpatrickalves/scraping-ebay/blob/master/scraping_ebay/spiders/ebay.py>

Similarly, instead of getting current product price or description data,
but rather to extract ebay sale data, refer to this script:
<https://github.com/cpatrickalves/scraping-ebay/blob/master/scraping_ebay/spiders/ebay_au_sold.py>

"""
#define the ebay product web crawler:
class web_eBay_crawler(scrapy.Spider):
    #define the name of the web crawler
    name = ebay_product
    #define which web domains the Spider is allowed to "crawl":
    allowed_domains = ['ebay.com']
    #specify  URL from which the Spider will start the web crawling
    start_urls = 'https://www.ebay.com'
    
