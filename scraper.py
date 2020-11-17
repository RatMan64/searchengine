# RileyBarnes Kelly
# cs454

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

# get dataset from the-house.com

# begining url
url = "https://www.the-house.com/boardshop.html"


regUrl = "www.The-House.com"


def firstPage():
    uClient = uReq(url)

    soup = bs(uClient.read(), "html.parser")
    uClient.close()
    # scrape for snowboards, snowbard jackets, snowboard pants, gloves, beanies, base layers, snowboard boots, bidings, helmets, goggles, bags.
    # feilds = item desc, picture, type, brand,  year, size, price, url, is onsale, gender

    headers = "itemDescription, picture,  Type, Brand, Year, Size, Price, Url, Onsale, Gender"
    out_filename = "SearchEngineData.csv"

    file = open(out_filename, "w", encoding='utf-8')
    file.write(headers)


    for catigory in catigory:
        








def grabItems(extentionUrl, itemType):
    uClient = uReq(regUrl+extentionUrl)
    cagigorysoup = bs(uClient.read(), "html.parser")
    uClient.close()
    itemDesc = ""
    picture = ""
    brand = ""
    year=""

    return

# snowBoards


# jackets


# pants

# gloves

# beanies

# base layers

# snowboard boots

# bindings


# helmet

# goggles

# bags