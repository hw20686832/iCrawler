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
    name = 'mop_tz'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('.content')

        content=content_node('.nr_con')
        if not content:
            content=content_node('.mainpart').eq(0)
        
        item = ContentItem()
        imgs = content('img')
        img_all = []
        for img in imgs:
            if not img.get('data-original'):
                if".gif" in img.get('src'):
                    continue
                else: 
                    imgs.eq(imgs.index(img)).append('<br>')
                    imgs.eq(imgs.index(img)).before('<br>')
                    img_all.append(self.getRealURI(img.get('src')))
            else: 
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                imgs.eq(imgs.index(img)).attr["src"] = img.get('data-original')
                img_all.append(self.getRealURI(img.get('data-original')))
        item['image_urls'] = img_all
        
        author=content_node('.nr_info')('a').eq(0).text()
        if not author:
            author=content_node('div.tzsm')('a').eq(0).text()
        release_time=doc('.nr_info').text()
        if not release_time:
            release_time=doc('div.tzsm').text()
        ob=re.compile(u'20\d\d-\d\d-\d\d \d\d:\d\d:\d\d')
        release_time=ob.findall(release_time)
        
        item['title'] = self.title = content_node('h1').text()
        item['content'] = self.content = content.__unicode__()
        item['release_time'] = release_time[0]
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time[0],u'%Y-%m-%d %H:%M:%S'))
        item['source'] = u"猫扑"
        item['author'] = author
        if not item['author']:
            author = doc('div.tzsm').find('a').eq(0).text()
        item['pic_url'] = ''
        
        self.title = item['title']
        self.content = item['content']
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False