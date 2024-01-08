import pandas as pd
import os
from pathlib import Path
import glob


# prompt user to specify which product keyword they want to analyze
product_name = input("Specify what product name keyword you want to analyze: ") 

# specify path
# NB: absolute path is: <<< r'D:\Coding and Code projects\Python\ebay_data_proj\ebay_price_data'
path = r''...

# import all CSV files from ebay_price_data matching given keyword
for files in glob.glob(path + '/*.csv'):
    csv = pd.read_csv(files)
    df = df.append(csv)



# calculate avg price by product condition
df.groupby("condition")['price'].agg('mean')

# calculate avg price by price type so we can compare Buy it now vs auctions
df.groupby("price_type")['price'].agg('mean')

# now, let's compare avg price by item condition AND price type, so we can more accurately assess whether New or Used items tend to have selling prices when sold via Auction vs Buy it now
df.groupby("condition", "price_type")['price'].agg('mean')

# now, let's examine Auctioned items and see whether avg prices are higher or lower on certain days of the week for Used or New items

# # group data by day using date_sold data
# data_by_day = df.groupby(pd.Grouper(key='date_sold', axis=0, freq='D')).sum()

# group the data by condition,  price_type, AND day of week!

df.groupby(["condition", "price_type", 'date_sold'.dt.weekday_name])['price'].agg('mean')

# 