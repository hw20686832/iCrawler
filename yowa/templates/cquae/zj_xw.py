#coding: utf-8

import re
import time
from pyquery import PyQuery
import Image
import string

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'zj_cquae'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('table[style = "background-color: #cccccc;"]')
        
        item = ContentItem()
        imgs = content_node('img')
        img_all = []
        for img in imgs:
            if ".gif" in img.get('src'):
                continue
            else:  
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                img_all.append(self.getRealURI(img.get('src')))
        item['image_urls'] = img_all
        
        self.title = doc('div.n_2').text()
        item['title'] = self.title
        item['content'] = self.content = content_node.__unicode__()
        deadline = self.hxs.select("//table[@style='background-color: #cccccc;'][1]//tr[3]/td[4]/text()").extract()
        if len(deadline) >0:
            item['deadline'] = string.strip(deadline[0]) 
        item['release_time'] = ''
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time,u'%Y��%m��%d��%H:%M'))
        item['source'] = u"重庆联合产权交易所"
        item['author'] = ''
        item['pic_url'] = ''
        item['city'] = u"重庆"
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
