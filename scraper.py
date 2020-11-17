# RileyBarnes Kelly
# cs454

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import time

# get dataset from the-house.com

# begining url
url = "https://www.the-house.com/boardshop.html"


regUrl = "www.The-House.com"


def firstPage():
    uClient = uReq(url)

    page_html = bs(uClient.read(), "html.parser")
    uClient.close()
    # scrape for snowboards, snowbard jackets, snowboard pants, gloves, beanies, base layers, snowboard boots, bidings, helmets, goggles, bags.
    # feilds = item desc, picture, type, brand,  year, size, price, url, is onsale, gender

    headers = "itemDescription, picture,  Type, Brand, Year, Size, Price, Url, Onsale, Gender"
    out_filename = "SearchEngineData.csv"

    file = open(out_filename, "w", encoding='utf-8')
    file.write(headers)


    for catigory in catigory:
        if catigory == "snowboard packages" or catigory == "snowboard acessories" or catigory == "snow skate, snow surfers":
        #if its a catigory that has sub classes add that to the grab items
        if catigory ==:
        








def grabItems(extentionUrl, itemType, hasSubCats):
    #first we look at the first page of the catigory we change the url as we have completed the page
    newClient = uReq(regUrl+extentionUrl)
    cagigorysoup = bs(newClient.read(), "html.parser")
    newClient.close()
    Type = itemType

    # while loop that writes each catigroy item to the file

    if(hasSubCats != True):

        while():



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




                time.sleep(5)


    else:










    return




def main():
    firstPage()

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