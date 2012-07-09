#coding: utf-8
'''
Created on 2012-3-27

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'miercn_tz'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.cc2')
        content_node.remove('script')
        content_node.remove('div.page1')
        content_node.remove('div[style = "padding-left:5px;"]')
        content_node.remove('style')
        
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
        
        item['title'] = self.title = doc('h1').text()
        content = content_node.__unicode__()
        content = content.replace(u'点击查看更多图片','')
        item['content'] = self.content = content
        
        release_time=doc('div.sj').text()
        ob=re.compile(u'20\d\d.*\d\d')
        release_time=ob.findall(release_time)
        
        item['release_time'] = release_time[0]
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time,u'%Y-%m-%d %H:%M:%S'))
        item['source'] = u"米尔社区"
        item['author'] = doc('div.sj')('font').eq(0).text()
        item['pic_url'] = ''
        
        self.title = item['title']
        self.content = item['content']
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False