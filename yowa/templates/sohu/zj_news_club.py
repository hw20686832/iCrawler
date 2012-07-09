#coding: utf-8
'''
Created on 2012-2-3

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from scrapy.selector import HtmlXPathSelector
from yowa.items import ContentItem

class Parser(Base):
    name = 'sohu_news_club'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = self.hxs.select("//div[@class = 'bA']/div[@id = 'pic']/a/img/@alt").extract()
        
        item = ContentItem()
        content_img = self.hxs.select("//div[@class = 'bA']/div[@id = 'pic']/a/img/@src").extract()

        item['image_urls'] = content_img
        
        item['title'] = self.title = doc('h1').text()
        self.content = '<img src="'+item['image_urls'][0]+'"><br><br>'+content_node[0]
        item['content'] = self.content
        item['release_time'] = ''
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time[0],u'%Y-%m-%d %H:%M'))
        item['source'] = u"搜狐"
        item['author'] = ''
        item['pic_url'] = ''

        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
