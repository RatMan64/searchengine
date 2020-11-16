#RileyBarnes Kelly
#cs454

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
#get dataset from the-house.com

#begining url
url = "https://www.the-house.com/boardshop.html"
uClient = uReq(url)

soup =bs(uClient.read(), "html.parser")
uClient.close()
#scrape for snowboards, snowbard jackets, snowboard pants, gloves, beanies, base layers, snowboard boots, bidings, helmets, goggles, bags.
# feilds = item desc, type, brand,  year, size, price, url, is onsale, gender

headers = "itemDescription, Type, Brand, Year, Size, Price, Url, Onsale, Gender"
out_filename = "SearchEngineData.csv"

file = open(out_filename,"w", encoding= 'utf-8' )
file.write(headers)

