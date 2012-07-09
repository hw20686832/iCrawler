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
    name = 'meituan_tg'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div[class = "mainbox cf"]').find('div.main') + doc('ul#biz-address-list')
        content_node.remove('div.banner-for-movie')
        content_node.remove('a.search-path')
        content_node.remove('a.view-map')
        content_node.remove('embed')
        
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
        price = doc('.deal-price')('strong').text()
        if not price:
            price = doc('div[class = "deal-buy deal-price-tag-open"]')('strong').text()
        p = re.compile(u'¥(.*)')
        price = p.search(price).group(1)
        item['price'] =self.price = price
        city = doc('.city')('h2')
        city.remove('a')
        item['city'] = self.city = city.text()
        item['release_time'] = ''
        
        deadline_s=time.time()
        deadline_d = doc('div[class = "deal-box deal-timeleft deal-on"]').attr('diff')
        if not deadline_d:
            deadline_d = doc('p[class = "deal-status-time-left deal-on"]').attr('diff')
        deadline_d = string.atoi(deadline_d)
        deadline = deadline_s + deadline_d
        deadline = time.localtime(deadline)
        item['deadline'] = time.strftime('%Y-%m-%d',deadline)

#        item['release_switch_time'] = self.release_switch_time = time.time()
        item['source'] = u"美团网"
        item['author'] = ''
        pic_url = [img.get('src') for img in doc('div#hd')('img')]
        item['pic_url'] = pic_url[0]
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False