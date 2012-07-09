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
    name = 'rayli_xw'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div#rightdiv1')
        content_node.remove('span.white12')
        item = ContentItem()
        content_node = content_node.__unicode__()
        img_all = []
        img='leftsmallimgurl\[1\]\=\"(.*?)\"\;'
        ob = re.compile(img)
        imgs = ob.findall(doc.__unicode__())
        if not imgs:
            image=''
        else:
            image='<br/><img src="'+imgs[0]+'"/><br/>'
            img_all.append(self.getRealURI(imgs[0]))
        content_node=image+content_node
        item['image_urls'] = img_all
                
        item['title'] = self.title = doc('h1').text()
        item['content'] = self.content = content_node
                    
        item['release_time'] = ''
#        item['release_switch_time'] = self.release_switch_time = time.time()
        item['source'] = u"瑞丽服饰网"
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