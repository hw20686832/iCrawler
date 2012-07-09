#coding: utf-8
'''
Created on 2012-2-13

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'dianping_tz'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)  
         
        item = ContentItem()        
        
        
        content_a = doc('a')
        for a in content_a:
            #content_a(content_a.index(a)).attr.href = self.getRealURI(a.get('href'))
            content_a(content_a.index(a)).attr.href = "www.dianping.com" + a.get('href')
            
        content_node1 = doc('div.content-main')
        content_node2 = doc('div.content-misc')
        content_node2.remove('span.misc')
        content_node2.remove('li.more')
        
        imgs = content_node1('img')
        img_all = []
        for img in imgs:
            if".gif" in img.get('src'):
                continue
            else:  
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                img_all.append(self.getRealURI(img.get('src')))
        item['image_urls'] = img_all
        item['title'] = self.title = doc('h1').text()
        content = content_node1.__unicode__() + content_node2.__unicode__()

        item['content'] = self.content = content
        item['source'] = u"点评网"
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False