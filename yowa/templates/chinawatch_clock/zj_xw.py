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
    name = 'chinawatch_clock_xw'

    def extract(self):
        item = ContentItem()
        self.html = re.sub('<!--.*?-->', '', self.html)
        
        xw_title=self.hxs.select("//table/tr/td[@class='title']/text()").extract()
        xw_content=self.hxs.select("//table/tr/td[@class='content']").extract()
        
        release_time=self.hxs.select("//table/tr/td[@class='t12deegrey']/text()").extract()
        ob=re.compile(u'20\d\d-\d*-\d*')
        for res in release_time:
            if not ob.findall(res):
                continue
            else:
                release_time=ob.findall(res)

        imgs = self.hxs.select("//table/tr/td[@class='content']/p/img/@src").extract()
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
        item['source'] = u"中国钟表"
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