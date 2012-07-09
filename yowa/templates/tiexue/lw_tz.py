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
    name = 'tiexue_tz'

    def extract(self):
        item = ContentItem()
        self.html = re.sub('<!--.*?-->', '', self.html)

        tz_title=self.hxs.select("//h1/text()").extract()
        content=self.hxs.select("//ul[@class='content']/li/div").extract()
        tz_content=''
        for con in content:
            if "fromposty" in con:
                tz_content=self.hxs.select("//ul[@class='content']/li/div")[2].extract()
                break
            else:
                tz_content=self.hxs.select("//ul[@class='content']/li/div")[1].extract()
        
        release_time=self.hxs.select("//div[@class='gray']/text()").extract()

        imgs=PyQuery(tz_content)
        ob=re.compile('src="(.*?)"')
        imgs=ob.findall(imgs.__unicode__())
        img_all=[]
        for img in imgs:
            if ".gif" in img:
                continue
            if ".GIF" in img:
                continue
            else:
                img_all.append(self.getRealURI(img))
                
        author=self.hxs.select("//td[@class='bbsname']/b/span/a/text()").extract()
        tz_content = PyQuery(tz_content)
        cont_div = tz_content('div[style = "color:#FCFCCC"]')
        for cont in cont_div:
            cont_div.eq(cont_div.index(cont)).removeAttr('style')
        tz_content = tz_content.__unicode__()
        item['image_urls'] = img_all
        item['title'] = self.title = tz_title[0].strip()
        item['content'] = self.content = tz_content
        item['release_time'] = ''
        item['source'] = u"铁血网"
        item['author'] = author[0]
    
        item['pic_url'] = ''
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(self.release_time,u'%Y-%m-%d %H:%M'))
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False