#coding: utf-8
'''
Created on 2012-4-26

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'shhbm_yh'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.con')
        content_node.remove('div.endSummary')
        content_node.remove('div.pb')
        
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
        
        release_time=doc('div.subtit').text()
        ob=re.compile(u'20\d\d.*-\d\d')
        release_time=ob.findall(release_time)
                
        content_node = content_node.__unicode__().replace(u'点击图片进入下一页','')
        content_node = content_node.replace(u'点击此处文字查看大图','')
        content_node = content_node.replace(u'点击文字查看大图','')
        item['title'] = self.title = doc('div.title').text()
        item['content'] = self.content = content_node
        item['release_time'] = release_time[0]
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time[0],u'%Y-%m-%d'))
        item['source'] = u"上海打折网"
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