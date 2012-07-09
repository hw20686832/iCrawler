#coding: utf-8
'''
Created on 2012-2-21

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'people_dn'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.show_text')
        if doc('div.text_img')('img'):
            content_node=doc('div.text_img')('img')+content_node
        
        del_a = content_node('center')
        del_a.remove('a')
        content_node.remove('table[bordercolor = "#999999"]')
        content_node.remove('table#table1')
        content_node.remove('div.zdfy.clearfix')
        content_node.remove('div[style = "margin:0 auto;text-align:center;"]')
        item = ContentItem()
        imgs = content_node('img')
        img_all = []
        for img in imgs:
            if ".gif" in img.get('src'):
                continue
            else:  
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                img_all.append(self.getRealURI(img.get('src')))
        item['image_urls'] = img_all
        
        self.title = doc('#p_title').text()
        if not self.title:
            self.title = doc('#title_tex').text()
        item['title'] = self.title
        item['content'] = self.content = content_node.html()
        release_time=doc('#p_publishtime').text()
        item['release_time'] = release_time
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time,u'%Y年%m月%d日%H:%M'))
        item['source'] = u"人民网"
        item['author'] = ''
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
