#coding: utf-8
'''
Created on 2012-4-24

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'bj100_yh'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)  
        content_node = doc('dl.sj_tp')+doc('div.sj_xx')+doc('div.yh_xx')+doc('div.yh_bt').eq(0)+doc('div.dybj').eq(0)+doc('p#sms_content')
        content_node.remove('a[href = "javascript:void(0)"]')
        item = ContentItem()        
        
        
        imgs = content_node('img')
        img_all = []
        for img in imgs:
            if".gif" in img.get('src'):
                continue
            if".GIF" in img.get('src'):
                continue
            else:  
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                img_all.append(self.getRealURI(img.get('src')))
        item['image_urls'] = img_all
        item['title'] = self.title = doc('h1').text()
        item['content'] = self.content = content_node.__unicode__()
#        item['merchant'] = ''
        
        deadline=doc('div.yh_ts').text()
        ob=re.compile(u'至(20\d\d.*-\d\d)')
        deadline=ob.findall(deadline)        
        item['deadline'] = deadline[0]
        item['source'] = u"京探网"
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False