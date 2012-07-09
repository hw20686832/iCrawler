#coding: utf-8

import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'zj_silver'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div#contentBody')
        content_node.remove('h3')
        content_node.remove('ul.xgyd1')
        content_node.remove('p[style = "margin-top:10px;"]')
        content_node.remove('div[style = "text-align:left; margin:10px; font-size:12px;"]')
        
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
        
        self.title = doc('h1').text()
        item['title'] = self.title
        item['content'] = self.content = content_node.__unicode__()
        release_time=doc('p.wenz_bq').text()
        r = re.compile(u"(20\d\d.*\d\d:\d\d)")
        self.release_time = r.search(release_time).group()
        item['release_time'] = self.release_time
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time,u'%Y��%m��%d��%H:%M'))
        item['source'] = u"第一白银网"
        item['author'] = ''
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
