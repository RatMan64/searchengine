# RileyBarnes Kelly
# cs454

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import time

# get dataset from the-house.com

# begining url
url = "https://www.the-house.com/boardshop.html"

# url extenstion
regUrl = "https://www.The-House.com"
headers = "itemName,itemDescription, picture,  Type, Brand, Year, Size, Price, Url, Onsale, discountr"
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
        # print(catigory)
        catigoryName = catigory.a.span["name"]
        # print(catigoryName)
        # print(type(catigoryName))

        urlExt = catigory.a["href"]
        # print(urlExt)

        # skip snow skaters
        if catigoryName == "Snow Skate, Snow Surfers"  or catigoryName == "Snowboard Packages":
            continue
        # if its a catigory that has sub classes go to the subcats function
        if catigoryName == "Snowboarding Clothes & Apparel" or catigoryName == "Snowboard Accessories" or catigoryName =="Splitboard Gear":
            subCats(urlExt)
        else:
            grabItems(urlExt,catigoryName)

    file.close()
#TODO! finish subcats
# sub cats is basically thefirst for loop but needs to be done as some catigorys have more catigorys
def subCats(extentionUrl):
    print("Sub Cats Entered")
    subClient = uReq(regUrl+extentionUrl)
    subsoup = bs(subClient.read(), "html.parser")
    subClient.close()
    time.sleep(5)
    cats = subsoup.findAll("div", {"class": "col-xs-6 skinny"})
    for cat in cats:
        catDetails = cat.find("div", {"class": "category-name"})
        #print(catDetails)
        catName = catDetails.strong.text
        Type = catName


        #Clothing accessories has more categorys
        if catName == "Clothing Accessories":
            continue
        preUrl =cat.find("a", {"class":"thumbnail text-center"})
        postUrl = preUrl["href"].replace(",","")

        grabItems(postUrl,catName)

    return


def grabItems(extentionUrl, itemType):
    print("grab Items entered " + itemType)
    # first we look at the first page of the catigory we change the url as we have completed the page
    newClient = uReq(regUrl + extentionUrl)
    cagigorysoup = bs(newClient.read(), "html.parser")
    newClient.close()
    time.sleep(5)
    Type = itemType
    items = cagigorysoup.findAll("div", {"class": "col-sm-3 col-xs-6 col-xs-print-3 pull-left"})
    grab(Type, items, regUrl+extentionUrl, cagigorysoup)
    return

def grab(Type, items,url, oldsoup ):
    lastPage = False
    count =1
    endofitems = oldsoup.findAll("a", {"aria-label": "Go to last page"})
    # print(endofitems)
    # print(endofitems[0]["href"])
    # print(url)
    # print(endofitems[0]["href"])
    while lastPage != True:
        if (url + "?nocache=1&refine.pagenumber=" + str(count)) == "https://www.The-House.com/" + endofitems[0]["href"]:
            lastPage = True

        #print(count)
        if count>1:

            page ="?nocache=1&refine.pagenumber="+str(count)
            newUrl = url+page
            newPageClient = uReq(newUrl)
            soup = bs(newPageClient.read(), "html.parser")
            newPageClient.close()
            time.sleep(5)
            items = soup.findAll("div", {"class": "col-sm-3 col-xs-6 col-xs-print-3 pull-left"})
        # print(len(items))
        # print(count)
        for item in items:


            onsale = "F"
            discount = ""
            name = item.div.div.a.img["alt"]
            picture = item.div.div.a.img["src"]
            brandtitle = item.findAll("meta",{"itemprop": "brand"})
            # print(brandtitle[0]["content"])
            brand = brandtitle[0]["content"]
            # print(repr(brand))
            # print(repr(picture))
            # print(repr(name))
            #year = ""
            sizes =item.findAll("div",{"class": "category-product-title sizelist clearfix"})
            # print(sizes)
            size = sizes[0].text

            size = size.replace("Size:","").replace(",","-").replace("\n","").replace("\t","").strip()
            # print(type(size))
            # print(repr(size))


            prePrice = item.findAll("span", {"itemprop": "price"})
            price = prePrice[0].text
            preurl = item.div.findAll("div", {"class": "category-product-title"})
            itemUrl = regUrl + preurl[0].a["href"]
            #print(itemUrl)
            pageClient= uReq(itemUrl)
            pagehtml = bs(pageClient.read(), "html.parser")
            time.sleep(5)
            pageClient.close()
            #print(pagehtml)
            predesc = pagehtml.findAll("div", {"id": "product-description"})
            if len(predesc) ==0:
                itemDesc =""
            else:
                #print(predesc)
                itemDesc = predesc[0].text


            # itemDesc= str(itemDesc).strip("\\t\\n")
            itemDesc = itemDesc.replace(",","").replace("\n","").replace("\t","").replace("\v","").replace("\r","").replace("\b", "").strip()
            # print(itemDesc)
            # print(repr(itemDesc))

            dis=item.findAll("span",{"class":"category-product-discount sale"})
            # print(dis)
            if len(dis) != 0:
                onsale = "T"
                discount = str(dis[0].text)
                discount = discount.replace("\t","").replace("\n","")
                # print(repr(discount))
            else:
                discount=""
            # feilds = name,item desc, picture, type, brand,  year, size, price, url, is onsale, gender
            print(name)
            #print(repr(str(name)+","+str(itemDesc) + ","+ str(picture)+ ","+ str(Type)+","+str(brand)+ ","+ str(size)+ ","+ str(price)+ ","+ str(itemUrl)+"," + onsale +"," + str(discount)))
            file.write(str(name)+","+str(itemDesc) + ","+ str(picture)+ ","+ str(Type)+","+str(brand)+ ","+ str(size)+ ","+ str(price)+ ","+ str(itemUrl)+"," + str(onsale)+"," + str(discount)+ "\n" )
        count +=1



def main():
    beginScrape()


main()

