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
    name = 'jjckb_dn'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('#newsdetail-content-text')
        
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
        
        release_time=doc('.black12').eq(0).text()
        ob=re.compile(u'20\d\d.*\d\d')
        release_time=ob.findall(release_time)
        
        item['title'] = self.title = doc('.black18').text()
        item['content'] = self.content = content_node.__unicode__()
        item['release_time'] = release_time[0]
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time[0],u'%Y-%m-%d'))
        item['source'] = u"经济参考网"
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False