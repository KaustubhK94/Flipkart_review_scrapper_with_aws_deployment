from flask import Flask,render_template,request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ureq

searchstring = "iphone11"

flip_url = "https://www.flipkart.com/search?q=" + searchstring

print(flip_url)

uclient = ureq(flip_url) #hit the URL
print(uclient)

flip_page = uclient.read()  #returns HTML corpus
# print(flip_page)
# uclient.close()

flip_html = bs(flip_page,"html.parser")
# print(flip_html)

# "https://www.flipkart.com/search?q=https://www.flipkart.com/apple-iphone-11-black-128-gb/p/itm8244e8d955aba?pid=MOBFWQ6BKRYBP5X8&lid=LSTMOBFWQ6BKRYBP5X8IBG6BS&marketplace=FLIPKART&q=iphone+11&store=tyy%2F4io&srno=s_1_2&otracker=search&otracker1=search&fm=Search&iid=253ea9f6-aaac-4072-8d26-0a22258f239b.MOBFWQ6BKRYBP5X8.SEARCH&ppt=hp&ppn=homepage&ssid=3m25xz730g0000001682311771930&qH=f6cdfdaa9f3c23f3"

big_box= flip_html.findAll("div",({"class":"_1AtVbE col-12-12"}))
# print(div_tag)

print( len(big_box))

box = big_box[2]

print(box)

print(box.div.div.a['href'])

productlink = "https://www.flipkart.com/search?q="+box.div.div.a['href']

print(productlink)


prod_request = requests.get(productlink)
print(prod_request)

prod_html = bs(prod_request.text,"html.parser")
print(prod_html)

comment_box = prod_html.find_all("div",{"class" : "_16PBlm"})

print(str(len(comment_box))+" ***")

print(comment_box[1])

# For Ratings
print(comment_box[1].div.div.div.div.text)

# For all the rating of the mentioned product
# for i in comment_box:
    # print(i.div.div.div.div.text)

# isolating the comment along with tag
print(comment_box[1].div.div.find_all("div",{"class":""}))


# Text from the comment itself
print(comment_box[1].div.div.find_all("div",{"class":""})[0].div.text)

# print(comment_box.div.div.find_all("div",{"class":""})[0].div.text)

for i in comment_box:
    print(i.div.div.find_all("div",{"class":""})[0].div.text)
    print("\n")

## Customer Name isolating the tag(the one who is commenting)
# name = comment_box[3].div.div.find_all("p",{"class":"_2sc7ZR _2V5EHH"})
# print(name)

# name = comment_box[1].div.div.find_all("p",{"class":"_2sc7ZR _2V5EHH"})
# print(name)


## Customer Name(the one who is commenting)
# name = comment_box[3].div.div.find_all("p",{"class":"_2sc7ZR _2V5EHH"})[0].text
# print(name)

# name = comment_box[1].div.div.find_all("p",{"class":"_2sc7ZR _2V5EHH"})[0].text
# print(name)

# for i in comment_box:
    # print(i.div.div.find_all("p",{"class":"_2sc7ZR _2V5EHH"})[0].text)

# comtag = comm_box.div.div.find_all('div',{"class":''})
# custcomm = comtag[0].div.text