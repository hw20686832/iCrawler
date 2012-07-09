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
    name = 'ynet_dn'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div#pzoom').eq(0)
        
        release_time=doc('.pd10').text()
        ob=re.compile(u'20\d\d.*\d\d')
        release_time=ob.findall(release_time)

        content_node.remove('.pd10')
        content_node.remove('div.vcopyurl')
        
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
        
        item['title'] = self.title = doc('.hclc10')('h1').text()
        item['content'] = self.content = content_node.__unicode__()
        item['release_time'] = release_time[0]
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time[0],u'%Y/%m/%d %H:%M:%S'))
        item['source'] = u"北青网"
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False