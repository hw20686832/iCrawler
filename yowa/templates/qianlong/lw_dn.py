#coding: utf-8
'''
Created on 2012-2-21

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'qianlong_dn'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('#content')
        
        item = ContentItem()
        release_time=doc('#Date').text()
        item['release_time'] = release_time
        item['title'] = self.title = doc('#content')('h1').text()
        
        content_node.remove('#urlAndDate')
        content_node.remove('#c_TopADb')
        content_node.remove('h1')
        content_node.remove('h2')
        
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
        
        self.content = content_node.__unicode__()
#        if not self.content:
#            self.content = content_node.__unicode__()
        item['content'] = self.content
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time,u'%Y-%m-%d %H:%M:%S'))
        item['source'] = u"千龙网"
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False