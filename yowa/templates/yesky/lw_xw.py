#coding: utf-8
'''
Created on 2012-3-28

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'yesky_xw'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.content')
        if not content_node:
            content_node = doc('div.article')
        if not content_node:
            content_node = doc('div.ArticleCnt')
        content_node.remove('script')
        
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
        
        release_time=doc('div.title').text()
        if not release_time:
            release_time=doc('div.info').text()
        if not release_time:
            release_time = doc('div[class = "title blue"]').find('div').text()
        ob=re.compile(u'20\d\d.*:\d\d')
        release_time=ob.findall(release_time)
        
        title=doc('div.title')('h1').text()
        if not title:
            title=doc('title').text()
        if not title:
            title = doc('h1').text()
        
        item['title'] = self.title = title
        item['content'] = self.content = content_node.__unicode__()    
                    
        item['release_time'] = release_time[0]
#        item['release_switch_time'] = self.release_switch_time = time.time()
        item['source'] = u"天极网"
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