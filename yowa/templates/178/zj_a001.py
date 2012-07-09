#coding: utf-8
import re
import time

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = '178001'
    

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div#text')

        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('script')

        

        content = content_node.__unicode__()

        item = ContentItem()
        

        item['title'] = self.title = doc('h1').text()
        if not self.title:
            item['title'] = self.title = doc('h2').eq(0).text()
            
        item['content'] = self.content = content
        
        time_s1 = '%Y-%m-%d'
        time_s2 = '%Y-%m-%d %H:%M:%S'
        
        self.release_time = doc('div[class = "title"]').text()
        p = re.compile(u"(20\d\d-.*:\d\d)")
        time_s = time_s2
        if not self.release_time:
            self.release_time = doc('div[class = "date"]').text()
            p = re.compile(u"(20\d\d-\d\d-\d\d)")
            time_s = time_s1
        item['release_time'] = self.release_time = p.search(self.release_time).group()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,time_s))
        item['source'] = u"178-魔兽世界"
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
