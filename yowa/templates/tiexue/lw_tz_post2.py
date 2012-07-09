#coding: utf-8
'''
Created on 2012-3-29

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'tiexue_tz_post2'

    def extract(self):
        item = ContentItem()
        self.html = re.sub('<!--.*?-->', '', self.html)

        tz_title=self.hxs.select("//h1/text()").extract()
        tz_content=self.hxs.select("//div[@class='text']").extract()
        release_time=self.hxs.select("//div[@class='user']/ul/li/text()").extract()
        ob=re.compile(u'20\d\d.*:\d\d')
        release_time=ob.findall(release_time[0])

        imgs=self.hxs.select("//div[@class='text']/div/div/p/a/img/@src").extract()
        img_all=[]
        for img in imgs:
            if ".gif" in img:
                continue
            if ".GIF" in img:
                continue
            else:
                img_all.append(self.getRealURI(img))
        
        item['image_urls'] = img_all
        item['title'] = self.title = tz_title[0]
        
        content = tz_content[0]
        content_html = PyQuery(content)
        cont_div = content_html('div[style = "color:#f9f9f9"]')
        for cont in cont_div:
            cont_div.eq(cont_div.index(cont)).removeAttr('style')
        content_html = content_html.__unicode__()
        item['content'] = self.content = content_html
        item['release_time'] = release_time[0]
        item['source'] = u"铁血网"
        item['author'] = ''
    
        item['pic_url'] = ''
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(self.release_time,u'%Y-%m-%d %H:%M'))
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False