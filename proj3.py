#!/usr/bin/python
# -*- coding: utf-8 -*-

print "Project3"

'''
 import urllib
 from bs4 import BeautifulSoup
 from bidi.algorithm import get_display
 html = urllib.urlopen('http://www.ynet.co.il')
 soup = BeautifulSoup(html,"lxml")
 list = soup.find_all("a")

 for item in list:
    if "?".decode("utf-8","ignore") in item.text:
             print item.text
 when bidi package is installed this is used to print rtl
 from bidi.algorithm import get_display
 print get_display(item,upper_is_rtl=True)
 stocks web site in bizportal:
 http://www.bizportal.co.il/shukhahon/bizmadadtab.shtml?Sug=2&Opt=&p_id=199
'''
import time
import mysql.connector
import urllib
from bs4 import BeautifulSoup
from bidi.algorithm import get_display
# import mechanize

# initializing a browser instance in mechanize
'''
br = mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
'''


'''
connecting
'''


# opening the bizportal stocks table html
html = urllib.urlopen('http://www.bizportal.co.il/shukhahon/bizmadadtab.shtml?Sug=2&Opt=&p_id=199')
soup = BeautifulSoup(html,'lxml')
list = soup.find_all("td")


cnx = mysql.connector.connect(user='root', password='pass1',host='127.0.0.1',database='new_db')
cursor = cnx.cursor()

count=1
location=-1
hitStock=-1
stocks = [u"???",u"??????"]

i=0

#while (count):
for i in range(0,2500):
    for item in list:
            location=location+1
            if item.text in stocks:
                    hitStock = stocks.index(item.text)
                    #print item
                    stockNum = list[location+8].text
                    link = item.find('a')
                    # just when using mechanize
                    # site = "http://www.bizportal.co.il/Quote/Stock/GeneralView/"+stockNum
                    site2=urllib.urlopen("http://www.bizportal.co.il/Quote/Stock/GeneralView/"+stockNum)
                    # r = br.open(site)
                    # stockSoup = BeautifulSoup(r.read(),'html5lib')
                    stockSoup = BeautifulSoup(site2,'html5lib')
                    stockList = stockSoup.find_all("div")
                    for stockItem in stockList:
                            if stocks[hitStock] in stockItem.text:
                                    if stockItem.attrs.has_key('class'):
                                            if "titleRight" in stockItem['class']:
                                                    stockItem.span.decompose()
                                                    value= stockItem.find("div").text.replace("\n","").replace(" ","").replace(",","")
                                                    inputString="insert into stocks values ("+stockNum+",NULL,"+value+")"
                                                    print inputString
                                                    cursor.execute(inputString)
                                                    cnx.commit()
                                                    print value
                                                    if hitStock == len(stocks)-1:
                                                        time.sleep(10)

    count=1
    location=-1


