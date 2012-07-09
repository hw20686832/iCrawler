#coding: utf-8
'''
Created on 2012-2-9

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'gome_tg'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        
        
        item = ContentItem() 
        content_image = doc('div.product').find('div.pic').find('img').attr('src')
        item['image_urls'] = [content_image,]
        
        content = doc('div.product').find('h2').text()
        
        image="<br/><br/><img src='"+content_image+"'>"
        content=content+image

        item['title'] = self.title = doc('div.product').find('h2').text()
        item['content'] = self.content = content
        price = doc('div.product').find('div.price').find('span').text()
        item['price'] = price 
        item['release_time'] = ''
#        item['release_switch_time'] = self.release_switch_time = time.time()
        item['source'] = u"国美"
        item['author'] = ''
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
