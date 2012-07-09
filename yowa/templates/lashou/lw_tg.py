#coding: utf-8
'''
Created on 2012-2-8

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
    name = 'lashou_tg'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div#deal_lazyload')
        if not content_node:
            content_node = doc('div.new_info')
            content_node.remove('h2').eq(0)
        
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
        
        item['title'] = self.title = doc('h1').text()
        item['content'] = self.content = self.title + content_node.__unicode__()
        price = doc('.c-buy-num').text()
        p = re.compile(u'¥(.*)')
        price = p.search(price).group(1)
        item['price'] =self.price = price
        item['release_time'] = ''
        
        deadline_s=time.time()
        deadline_d = doc('div#sec_left').text()
        if not deadline_d:
            deadline_d = doc('span#sec_left').text()
        deadline_d = string.atoi(deadline_d)
        deadline = deadline_s + deadline_d
        deadline = time.localtime(deadline)
        item['deadline'] = time.strftime('%Y-%m-%d',deadline)
        
#        item['release_switch_time'] = self.release_switch_time = time.time()
        item['source'] = u"拉手网"
        item['author'] = ''
        pic_url = [img.get('src') for img in doc('div.c-pro-image')('img')]
        if not pic_url:
            pic_url = [img.get('src') for img in doc('div.package')('img')]
        item['pic_url'] = pic_url[0]
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False