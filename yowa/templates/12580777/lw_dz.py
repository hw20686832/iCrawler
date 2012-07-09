#coding: utf-8
'''
Created on 2012-4-26

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = '12580777_dz'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div[class="sib-img"]') + doc('ul[class="si-desc"]')
        content_node.remove('span.discount')
        
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
                
        item['title'] = self.title = doc('h3[class="si-name"]').text()
        
        content_node = content_node.__unicode__().replace(u'公交','')
        content_node = content_node.replace(u' | ','')
        content_node = content_node.replace(u'驾车','')
        item['content'] = self.content = content_node
        item['release_time'] = ''
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time[0],u'%Y-%m-%d'))
        item['source'] = u"12580商户联盟"
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