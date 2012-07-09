#coding: utf-8
'''
Created on 2012-2-13

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'eastmoney_tz_look'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('.neirong').eq(0)
        
        item = ContentItem()
        imgs = content_node('img')
        img_all = []
        for img in imgs:
            if".gif" in img.get('src'):
                continue
            else:  
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                img_all.append(self.getRealURI(img.get('src')))
        item['image_urls'] = img_all
        
        item['title'] = self.title = content_node('.biaoti').text()
        item['content'] = self.content = content_node('.huifu').__unicode__()
        
        release_time=content_node('.zuozhe').eq(0).text()
        ob=re.compile(u'20\d\d-.*\d\d')
        release_time=ob.findall(release_time)
        
        item['release_time'] = release_time[0]
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time[0],u'%Y-%m-%d %H:%M:%S'))
        item['source'] = u"东方财富网"
        item['author'] = ''
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False