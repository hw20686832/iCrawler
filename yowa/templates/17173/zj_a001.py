#coding: utf-8
import re
import time

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = '17173001'
    #17173

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div#matterc')
        if not content_node:
            content_node = doc('div[class = "newDescribe2 fs14"]')
        if not content_node:
            content_node = doc('div#matter')
            
        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('div.pagination')
        

        content = content_node.__unicode__()

        item = ContentItem()
        item['title'] = self.title = doc('h1').text()
        
        item['content'] = self.content = content
        
        self.release_time = doc('div.navFunction').text()
        p = re.compile(u"(20\d\d-\d\d-\d\d)")
        if not self.release_time:
            self.release_time = doc('div.newsAttribute').text()
        if not self.release_time:
            self.release_time = doc('div.newsAttribute').find('span.f1').eq(0).text()
            p = re.compile(u"(20.*)")
        item['release_time'] = self.release_time = p.search(self.release_time).group()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d'))
            
        item['source'] = u"17173"
        item['author'] = ''
        item['pic_url'] = ''

        imgs = content_node('img')
        image_urls = []
        for img in imgs:
            if ".gif" in img.get('src'):
                continue
            if not img.get('src'):
                continue
            else:
                image_urls.append(self.getRealURI(img.get('src')))
        item['image_urls'] = image_urls

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
