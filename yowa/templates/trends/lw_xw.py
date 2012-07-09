#coding: utf-8
'''
Created on 2012-4-23

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'trends_xw'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('td#acontent')
        
        item = ContentItem()
        img_all = []
        img='fristPicURL \= \"(.*?)\"\;'
        ob = re.compile(img)
        imgs = ob.findall(content_node.__unicode__())

        if not imgs:
            image=''
        else:
            image='<br/><img src="'+imgs[1]+'"/><br/>'
            img_all.append(imgs[1])
        
        content_node.remove('script')
        content_node.remove('div#imgslide')
        content_node = content_node.__unicode__()
        content_node=image+content_node
        
        release_time=doc('td#adate_source').text()
        ob=re.compile(u'20\d\d.*\d\d')
        release_time=ob.findall(release_time)
        
        item['image_urls'] = img_all
                
        item['title'] = self.title = doc('h1#atitle').text()
        item['content'] = self.content = content_node   
                    
        item['release_time'] = release_time[0]
#        item['release_switch_time'] = self.release_switch_time = time.time()
        item['source'] = u"时尚网"
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