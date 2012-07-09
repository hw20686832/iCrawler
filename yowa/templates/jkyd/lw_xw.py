#coding: utf-8
'''
Created on 2012-3-8

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'jkyd_xw'

    def extract(self):
        item = ContentItem()
        self.html = re.sub('<!--.*?-->', '', self.html)
        
        xw_title=self.hxs.select("//h1/text()").extract()
        xw_content=self.hxs.select("//span[@style='font-size: 14px; line-height: 150%']/p").extract()
        if not xw_content:
            xw_content=self.hxs.select("//span[@style='font-size: 14px; line-height: 150%']").extract()

        imgs = self.hxs.select("//span[@style='font-size: 14px; line-height: 150%']/img/@src").extract()
        img_all = []
        for img in imgs:
            if".gif" in img:
                continue
            if".GIF" in img:
                continue
            else:  
                img_all.append(self.getRealURI(img))
        item['image_urls'] = img_all
                
        item['title'] = self.title = xw_title[0]
        content_pq = PyQuery(xw_content[0])
        if not content_pq.text():
            item['content'] = self.content = xw_content[1]
        else:
            item['content'] = self.content = xw_content[0]        
        item['release_time'] = ''
#        item['release_switch_time'] = self.release_switch_time = time.time()
        item['source'] = u"健康有道"
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