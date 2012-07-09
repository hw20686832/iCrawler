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
    name = 'mypethome_tz'

    def extract(self):
        item = ContentItem()
        self.html = re.sub('<!--.*?-->', '', self.html)
        
        tz_title=self.hxs.select("//a[@id='thread_subject']/text()").extract()
        tz_content=self.hxs.select("//div[@class='t_fsz']/table/tr/td").extract()
        tz_author=self.hxs.select("//div[@class='authi']/a/text()").extract()
        tz_time=self.hxs.select("//div[@class='authi']/em/text()").extract()
        ob=re.compile(u'20\d\d.*\d\d')
        tz_time=ob.findall(tz_time[0])

        imgs = self.hxs.select("//div[@class='t_fsz']/table/tr/td/img/@src").extract()
        img_all = []
        for img in imgs:
            if".gif" in img:
                continue
            if".GIF" in img:
                continue
            else:
                img_all.append(self.getRealURI(img))
        item['image_urls'] = img_all
                
        item['title'] = self.title = tz_title[0]
        item['content'] = self.content = tz_content[0]        
        item['release_time'] = tz_time[0]
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(tz_time[0],u'%Y-%m-%d %H:%M:%S'))
        item['source'] = u"宠物之家"
        item['author'] = tz_author[0]
        item['pic_url'] = ''
        
        self.title = item['title']
        self.content = item['content']
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False