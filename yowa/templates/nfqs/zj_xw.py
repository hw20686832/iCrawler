#coding: utf-8
'''
Created on 2012-3-7

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'nfqs_xw'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('td[class= "news-td-text style12"][colspan="2"]').eq(1)
        
        item = ContentItem()
        imgs = content_node('img')
        img_all = []
        for img in imgs:
            if".gif" in img.get('src'):
                continue
            else:  
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                img_all.append(self.getRealURI(img.get('src')))
        item['image_urls'] = img_all
        
        item['title'] = self.title = doc('td[class= "news-td-text style12"][colspan="2"]').eq(0).text()
        item['content'] = self.content = content_node.__unicode__() 
            
        release_time=doc('td[class= "news-td-text style12"][align="right"]').text()
        ob=re.compile(u'20\d\d.*?:\d\d')
        release_time=ob.search(release_time).group()       
        item['release_time'] = release_time
#        item['release_switch_time'] = self.release_switch_time = time.time()
        item['source'] = u"国家食品质量安全"
        item['author'] = ''
        item['pic_url'] = ''
        
        self.title = item['title']
        self.content = item['content']
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False