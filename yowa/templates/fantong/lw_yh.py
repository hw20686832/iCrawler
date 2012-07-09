#coding: utf-8
'''
Created on 2012-4-24

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'fantong_yh'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)  
        content_node = doc('ul.store-info')+doc('div.detail-box-content')
        
        item = ContentItem()        
        
        
        imgs = content_node('img')
        img_all = []
        for img in imgs:
            if".gif" in img.get('src'):
                continue
            if".GIF" in img.get('src'):
                continue
            else:  
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                img_all.append(self.getRealURI(img.get('src')))
        item['image_urls'] = img_all
        item['title'] = self.title = doc('h1').text()
        item['content'] = self.content = content_node.__unicode__()
        item['merchant'] = doc('ul.store-info')('li')('a').text()
        
        deadline=doc('ul.store-info')('li').text()
        ob=re.compile(u'\- (20\d\d.*\d\d日)')
        deadline=ob.findall(deadline)        
        item['deadline'] = deadline[0]
        item['source'] = u"饭统网"
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False