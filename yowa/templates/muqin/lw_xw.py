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
    name = 'muqin_xw'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('span.word')
        content_node.remove('img')
        item = ContentItem()
#        imgs = content_node('img')
#        img_all = []
#        for img in imgs:
#            if".gif" in img.get('src'):
#                continue
#            else:  
#                imgs.eq(imgs.index(img)).append('<br>')
#                imgs.eq(imgs.index(img)).before('<br>')
#                img_all.append(self.getRealURI(img.get('src')))
#        item['image_urls'] = img_all
                
        item['title'] = self.title = doc('span.title')('b').text()
        item['content'] = self.content = content_node.__unicode__()    
        
        release_time=doc('span.about').text()
        ob=re.compile(u'20\d\d.*日')
        release_time=ob.findall(release_time)
        
        item['release_time'] = release_time[0]
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time[0],u'%Y年%m月%d日'))
        item['source'] = u"中国母亲网"
        item['author'] = ''
        item['pic_url'] = ''
        item['image_urls'] = []
        
        self.title = item['title']
        self.content = item['content']
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False