#coding:utf-8
import urlparse
import urllib2
import urllib
from BeautifulSoup import BeautifulSoup
import chardet
import pymongo
import time
from string import count
import os
# db = pymongo.Connection().notice #user notice

print("helloworld")

parseTuple = urlparse.urlparse("http://borqstom.borqs.com/MediaLibrary/")

print(parseTuple)

def getUrlData(webUrl):
    print("getUrlData " + webUrl)
    req = urllib2.Request(urllib.quote(webUrl, "://"), headers={'User-Agent' : "Magic Browser"})
    webPage = urllib2.urlopen(req)
    data = webPage.read()
    charset = chardet.detect(data)['encoding'].lower()
    if charset == 'gb2312':
        charset = 'GBK'
    soup = BeautifulSoup(data, fromEncoding = charset)
    lst = soup.findAll('a')
    url_set = []
    for item in lst:
        url = item.attrs[0][1]
        text = item.getText()
        url_set.append(url)
#         print(url)
#         print(text)
        indexup = text.rfind("Up To")
        if indexup != -1:
            continue 
        index = text.rfind('/')
#         print(index)
        if index == -1:
            print("wget " + webUrl + text)
            fileExist = os.path.exists(text)
            if fileExist == False:
                print("urllib.urlretrieve get " + text)
                urllib.urlretrieve(urllib.quote(webUrl + text, "://"), text)
            else:
                print(text + " already exist")
        else:
            print("mkdir " + text)
            print("cd " + text)
            dirExist = os.path.exists(text)
            if dirExist == False:
                os.mkdir(text)
            os.chdir(text)
            getUrlData(webUrl + text)
            
    print("cd ..")
    os.chdir("..")

     
print("=====begin======")
webUrl = "http://borqstom.borqs.com/MediaLibrary/"
getUrlData(webUrl)

print('=====end======')
# print(u)
