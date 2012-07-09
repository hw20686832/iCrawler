#coding: utf-8
'''
Created on 2012-2-9

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image
import string

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = '12580777_tg'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        
        
        item = ContentItem() 
        content_image = doc('img.pic_img').attr('src')
        item['pic_url'] = content_image
        
        content = doc('div.d_p').eq(0)
        
        imgs = content('img')
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

        item['title'] = self.title = doc('h1').find('b').text()
        item['content'] = self.content = self.title + content.__unicode__()
        price = doc('div.pr').text()
        p = re.compile(u'¥(.*)')
        price = p.search(price).group(1)
        item['price'] = price 
        item['release_time'] = ''
#        item['release_switch_time'] = self.release_switch_time = time.time()
        item['source'] = u"12580"
        item['author'] = ''
        
        deadline_d = doc('div[class = "lianjie"]').find('input').attr('value')
        deadline = string.atoi(deadline_d)
        deadline = time.localtime(deadline)
        item['deadline'] = time.strftime('%Y-%m-%d',deadline)
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
