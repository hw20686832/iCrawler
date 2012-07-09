#coding: utf-8
'''
Created on 2012-3-27

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'bitauto_xw'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.con_main')
        
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
        
        item['title'] = self.title = doc('h1')('a').text()        
        item['release_time'] = doc('li#time').text()
        
        content_node.remove('h1.con')
        content_node.remove('ul.con_time')
        content_node.remove('div.con_ad')
        content_node.remove('div#city')
        content_node.remove('div.con_pagelist')
        content_node.remove('table.con_nav')
        content_node.remove('div.the_pages')
        
        item['content'] = self.content = content_node.__unicode__()
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time,u'%Y-%m-%d %H:%M:%S'))
        item['source'] = u"联合越野"
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