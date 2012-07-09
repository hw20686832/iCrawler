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
    name = 'jinantuan_tg'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        
        
        
        item = ContentItem() 
        
        item['source'] = u"我爱团购"
        item['pic_url'] = ''

        
        return item

    def isMatch(self, ):
        return True
