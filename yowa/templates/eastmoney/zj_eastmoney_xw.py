#coding: utf-8
'''
Created on 2012-2-8

@author: joyce
'''
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'eastmoney_xw_zj'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('#ContentBody')
        
        item = ContentItem()
        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('script')
        content_node.remove('div.reading')
        content_node.remove('div.reading_bull')
        
        title = doc('h1').text()
        
        item['content'] = self.content = content_node.__unicode__()
        self.release_time = doc('div.Info').text()
        p = re.compile(u"(20\d\d.*\d\d:\d\d)")
        item['release_time'] = self.release_time = p.search(self.release_time).group()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y年%m月%d日 %H:%M'))
        item['title'] = self.title = title
        item['source'] = u"东方财富网"
        item['author'] = ''
        
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
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False