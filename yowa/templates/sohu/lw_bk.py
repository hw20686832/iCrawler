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
from yowa.items import ContentItem

class Parser(Base):
    name = 'sohu_bk'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('#main-content')
        content_node.remove('.pn_na')
        content_node.remove('div.shareToTblog')
        content_node.remove('div[style = "margin-top: 15px;float: right; height: 23px; border: #dfac63 1px solid; -webkit-border-radius: 4px; -moz-border-radius: 4px; border-radius: 4px;"]')
        
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
        
        item['title'] = self.title = doc('#entry')('h3').text()
        item['content'] = self.content = content_node('p').__unicode__()
        if not item['content']:
            item['content'] = self.content = content_node.__unicode__()
        item['release_time'] = self.release_time = doc('.revoRight').text()
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time[0],u'%Y-%m-%d %H:%M'))
        item['source'] = u"搜狐"
        item['author'] = doc('div.revoMyname').text()
        item['pic_url'] = ''

        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
