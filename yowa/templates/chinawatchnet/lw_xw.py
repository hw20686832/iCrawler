#coding: utf-8
'''
Created on 2012-3-26

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector
from yowa.items import ContentItem

class Parser(Base):
    name = 'chinawatchnet_xw'

    def extract(self):
        item = ContentItem()
        self.html = re.sub('<!--.*?-->', '', self.html)
        
        xw_title=self.hxs.select("//div/h1/text()").extract()
        xw_content=self.hxs.select("//div[@id='Text']").extract()
        
        release_time=self.hxs.select("//div[@class='info']/text()").extract()
        ob=re.compile(u'20\d\d.*\d\d')
        release_time=ob.findall(release_time[0])

        imgs = self.hxs.select("//div[@id='Text']/p/img/@src").extract()
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
        item['content'] = self.content = xw_content[0]        
        item['release_time'] = release_time[0]
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time[0],u'%Y-%m-%d'))
        item['source'] = u"中国钟表网"
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