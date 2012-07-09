#coding=utf-8
'''
Created on 2009-9-7

@author: Ken
'''
import  urllib
import urllib2
import random
import os
import sys
from sgmllib import SGMLParser
#from yowa.utils import ParserManager, urltools
from twisted.internet import reactor
from twisted.web import client
from scrapy.http import HtmlResponse
from optparse import OptionParser

class URLLister(SGMLParser):
    '''获取html中的图片地址\url地址，装入list中'''
    def reset(self):
        SGMLParser.reset(self)
        self.img = []
        self.urls = []
    def start_img(self, attrs):
        img = [v for k, v in attrs if k=='src']
        if img:
            self.img.extend(img)
    def start_a(self, attrs):
        href = [v for k, v in attrs if k=='href']
        if href:
            self.urls.extend(href)
class Crawl:
    def __init__(self, url):
        self.url = url
        self.response = None

    def result(self, body):
        self.response = HtmlResponse(url = self.url, body = body)
        reactor.stop()

    def fetch(self):
        deferred = client.getPage(self.url)
        deferred.addCallback(self.result)

        reactor.run()

def is_img(url):
    global imglenth
    request=urllib2.Request(url)
    opener=urllib2.build_opener()
    try:
        con=opener.open(request)
        Type=con.headers.dict['content-type'][:5] #判断链接返回的 content-type是不是图片。
        Length =int(con.headers.dict['content-length'])#判断图片大小
        if Length>imglenth:
            return Type
        else:
            return 0
    except:
        print '该图片无法在服务器找到或者图片地址无法识别！'
        print url

def get_file_name(ospath,imgname):
    name = 'P'+str(random.randint(10000000,99999999))
    filepath = "%s%s.%s" % (ospath,name,(imgname.split('.'))[-1])
    return filepath
def get_img(rq):
    parser = URLLister();    doc=Crawl(rq); doc.fetch();   parser.feed(doc.response.body);    img = parser.img
    parser.close()
    for i in range(0,len(img)):
        if img[i][0:4]!='http':#处理绝对路径
            img[i]=rq+img[i]
    print img
    return img

def get_url(rq):
    parser = URLLister();    doc=get_docum(rq);    parser.feed(doc);    urls = parser.urls
    parser.close()
    for i in range(0,len(urls)):
        if urls[i][0:4] != 'http': #处理绝对路径
            urls[i] = rq+urls[i]
    return urls

def depth(url,dep,ospath):
    '''三个参数分别是
    url ： 需要下载的网站地址
    dep ：需要遍历的深度
    ospath：图片下载的本地文件夹
    '''
    global num
    if dep<=0:
        return 0
    else:
        img=get_img(url)
        for j in range(0,len(img)):
            if is_img(img[j]) == 'image':
                isExist = True;
                while(isExist): #判断文件是否已经存在
                    filepath = get_file_name(ospath,img[j]);
                    if (not os.path.exists(filepath)):
                        isExist = False;
                try:
                    urllib.urlretrieve(img[j], filepath)
                    print '已经下载好第%d张图片'%(num+1)
                    num+=1
                except:
                    print '该图片无法下载或者图片地址无法识别！'
                    print img[j]
            else:
                pass
        urls=get_url(url)
        if len(urls)>0:
            for url in urls:
                depth(url,dep-1,ospath)
        else:
            return 0
        return 1


if __name__ == '__main__':
    imglenth = 1           #设置需要下载的图片大小。
    num=0
    depth('http://news.sina.com.cn/c/2012-05-23/021924460386.shtml',1,"/home/zhuj/")
    print '********************************我爬完了！！******************************************'
