#coding: utf-8
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'duowan001'
    #多玩

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div#text')
        content_node.remove('script[type = "text/javascript"]')
        #content_node.remove('style')
        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('div#pageNum')
        

        content = content_node.__unicode__()

        item = ContentItem()
        item['title'] = self.title = doc('h1').text()
        if item['title'] ==None:
            item['title'] = self.title = doc('div#title').find('h2').eq(0).text()
        
        item['content'] = self.content = content
        self.release_time = doc('address').text()
        p = re.compile(u"(20.*:\d\d)")
        if not self.release_time:
            self.release_time = doc('span.articledate').text() 
        if not self.release_time:
            self.release_time = doc('p#articleinfo').text()
        if not self.release_time:
            self.release_time = doc('div.articleinfo').text()
            
        item['release_time'] = self.release_time = p.search(self.release_time).group()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d %H:%M:%S'))
            
        item['source'] = u"多玩"
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
