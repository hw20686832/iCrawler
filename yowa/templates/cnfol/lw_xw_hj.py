#coding: utf-8
'''
Created on 2012-3-13

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from scrapy.selector import HtmlXPathSelector
from yowa.items import ContentItem

class Parser(Base):
    name = 'cnfol_xw_hj'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.pageBd')
        if not content_node:
            content_node = doc('div[id = "__content"]')
        
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
        
        release_time=doc('div.EDArt')('label').text()
        if not release_time:
            release_time = doc('div[class = "wzy2L3-1"]').text()
        ob=re.compile(u'20\d\d.*:\d\d')
        release_time=ob.findall(release_time)
                
        item['title'] = self.title = doc('h1').text()
        if not self.title:
            item['title'] = self.title = doc('div[class = "wzy2L1"]').text()
            
        content_node = content_node.__unicode__()
        content_node = content_node.replace('\r\n','')
        item['content'] = self.content = content_node
        item['release_time'] = release_time[0]
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time[0],u'%Y-%m-%d %H:%M'))
        item['source'] = u"中金在线"
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