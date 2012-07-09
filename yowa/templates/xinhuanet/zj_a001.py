#coding: utf-8
import re
import time

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'xinhua001'
    

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div#Content')
        if not content_node:
            content_node = doc('div#contentblock')
        if not content_node:
            content_node = doc('td.p1')
            content_node.remove('table')

        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('script')
        content_node.remove('div#div_currpage')
        content_node.remove('div#div_page_roll1')
        

        content = content_node.__unicode__()

        item = ContentItem()
        

        self.title = doc('span#title').text()
        if not self.title:
            self.title = doc('td.txt18').text()
        if not self.title:
            self.title = doc('div#Title').text()
        if not self.title:
            self.title = doc('h1#title').text()
        item['title'] = self.title    
        
        item['content'] = self.content = content
        
        self.release_time = doc('span[id = "pubtime"]').text()
        p = re.compile(u"(20\d\d.*:\d\d)")
        if not self.release_time:
            self.release_time = doc('td[class = "hei12"][align = "center"]').text()
        if not self.release_time:
            self.release_time = doc('td.wht12').text()
        item['release_time'] = self.release_time = p.search(self.release_time).group()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y年%m月%d日 %H:%M:%S'))
                    
        item['source'] = u"新华网"
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
