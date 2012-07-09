#coding: utf-8

import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'zj_cfi'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div#tdcontent')
        
        
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
        
        release_time=doc('td[style = "font-size:9pt;text-align:center;padding:3px 0px 5px 3px"]').text()
        r = re.compile(u"(20\d\d.*\d\d:\d\d)")
        self.release_time = r.search(release_time).group()
        item['release_time'] = self.release_time
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time,u'%Y��%m��%d��%H:%M'))
        content_node.remove('h1')
        content_node.remove('table[style = "margin:0 0px 0 0px"]')
        content_node.remove('table[style = "border-style: solid;border-color: rgb(200,200,200);border-width:1;width:100%;background-color=rgb(240,240,240)"]')
        
        item['content'] = self.content = content_node.__unicode__()
        item['source'] = u"中财网"
        item['author'] = ''
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
