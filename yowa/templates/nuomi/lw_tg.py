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
    name = 'nuomi_tg'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.goods_fl')
        
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

        #item['title'] = self.title = ', '.join((doc('div.details')('h2').text(), doc('div.details')('p.dp').text()))
        if doc('div.details')('h2').text():
            item['title'] = self.title = doc('div.details')('h2').text() + doc('div.details')('p.dp').text()
        if doc('div.details')('h1').text():
            item['title'] = self.title = doc('div.details')('h1').text() + doc('div.details')('p.dp').text()
        item['content'] = self.content = self.title + content_node.__unicode__()
        price = doc('.dm_buy')('p').text()
        item['price'] = price = price.encode('utf-8').replace('¥','')
        item['city'] = self.city = doc('.change_city')('strong').text()
        item['release_time'] = ''
#        item['release_switch_time'] = self.release_switch_time = time.time()
        item['source'] = u"糯米网"
        item['author'] = ''
        pic_url = [img.get('src') for img in doc('div.dm_img')('img')]
        item['pic_url'] = pic_url[0]
        
        deadline = doc('div[class = "sep countdown"]').attr('endtime')
        deadline = deadline[0:10]
        deadline = string.atoi(deadline)
        deadline = time.localtime(deadline)
        item['deadline'] = time.strftime('%Y-%m-%d',deadline)
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
