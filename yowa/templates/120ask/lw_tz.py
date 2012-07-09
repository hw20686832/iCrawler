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
    name = '120ask_tz'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node1 = doc('div.d_msCon')
        content_node2 = doc('div[class="crazy"]')
        content = content_node1.__unicode__()
        content = content + "<p>================</p>"
        n = 0
        for cont in content_node2:
            n = content_node2.index(cont)+1
            content = content + "<p> " + str(n) +u" 楼</p>"
            content = content + content_node2.eq(content_node2.index(cont)).__unicode__()
            content = content + "<p>-----------------</p>"
        
        item = ContentItem()
        imgs = content_node1('img')
        img_all = []
        for img in imgs:
            if".gif" in img.get('src'):
                continue
            else:  
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                img_all.append(self.getRealURI(img.get('src')))
        item['image_urls'] = img_all
        
        item['title'] = self.title = doc('#d_askH1').text()
        item['content'] = self.content = content
        
        release_time=doc('div.d_r').text()
        ob=re.compile(u'20\d\d.*\d\d')
        release_time=ob.findall(release_time)
        
        item['release_time'] = release_time[0]
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time[0],u'%Y-%m-%d %H:%M:%S'))
        item['source'] = u"有问必答网"
        
        author=doc('div.d_r')('a').text()
        if not author:
            author="医苑会员"
        
        item['author'] = author        
        item['pic_url'] = ''
        
        self.title = item['title']
        self.content = item['content']
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False