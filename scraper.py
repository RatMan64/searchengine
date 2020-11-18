# RileyBarnes Kelly
# cs454

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import time

# get dataset from the-house.com

# begining url
url = "https://www.the-house.com/boardshop.html"

# url extenstion
regUrl = "www.The-House.com"
headers = "itemDescription, picture,  Type, Brand, Year, Size, Price, Url, Onsale, Gender"
out_filename = "SearchEngineData.csv"

file = open(out_filename, "w", encoding='utf-8')
file.write(headers)


def beginScrape():
    uClient = uReq(url)
    page_html = bs(uClient.read(), "html.parser")
    uClient.close()
    catigorys = page_html.findAll("div", {"class": "col-xs-6 skinny"})
    time.sleep(5)
    # scrape for snowboards, snowbard jackets, snowboard pants, gloves, beanies, base layers, snowboard boots, bidings, helmets, goggles, bags.
    # feilds = item desc, picture, type, brand,  year, size, price, url, is onsale, gender

    for catigory in catigorys:
        catigoryDetails = catigory.find("div", {"class": "category-name"})
        catigoryName = catigoryDetails.span.name

        # skip snow skaters
        if catigoryName == "Snow Skate, Snow Surfers":
            continue
        # if its a catigory that has sub classes add that to the grab items
        if catigoryName == "SnowBoarding Clothes & Apparel":
            subCats()
        else:
            grabItems()

    file.close()


def subCats(extentionUrl):
    subClient = uReq(regUrl+extentionUrl)
    subsoup = bs(subClient.read(), "html.parser")
    subClient.close()
    time.sleep(5)
    cats = subsoup.findAll("div", {"class": "col-xs-6 skinny"})
    for cat in cats:

    return


def grabItems(extentionUrl, itemType):
    # first we look at the first page of the catigory we change the url as we have completed the page
    newClient = uReq(regUrl + extentionUrl)
    cagigorysoup = bs(newClient.read(), "html.parser")
    newClient.close()
    time.sleep(5)
    Type = itemType

    # while loop that writes each catigroy item to the file

    for item in items:
        itemDesc = ""
        picture = ""
        brand = ""
        year = ""
        size = ""
        price = ""
        url = ""
        onsale = ""
        Gender = ""

    return


def main():
    beginScrape()


main()

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
