#coding: utf-8
'''
Created on 2012-2-13

@author: joyce
'''
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'sohu_tz'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div#contentText')
        
        content_node.remove('script')
        content_node.remove('style')
        content_node.remove('.line')
        content_node.remove('#shareIn')
        content_node.remove('.tagHotg')
        content_node.remove('.blank8')
        content_node.remove('."editShare clear"')
        content_node.remove('select')
        #content_node.remove('table[width = "100%"]')('td[align = "center"]')
        content_node.remove('div[class = "jingbian_travel01_04"]')
        content_node.remove('div[class = "txt2"]')
        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('td[style = "font-size: 14px; font-weight: bold;"]')
        content_node.remove('table[style = "margin-right: 20px;"]')
        content_node.remove('digi_perpage_bottom')
        content_node.remove('div[class = "extract clear"]')
        content_node.remove('table[bgcolor = "#eeeeee"]')
        content_node.remove('img[alt = "搜狐教育频道"]')
        content_node.remove('table[bgcolor = "#e2e2e2"]')
        content_node.remove('table[bgcolor = "#66ccff"]')
        content_node.remove('div[class = "digi_digest"]')
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
        item['content'] = self.content = content_node.__unicode__()
        t = re.compile(u'var club_artinputdate = "(.*?)";')
        release_time = t.search(doc.html())
        if release_time:
            item['release_time'] = self.release_time = release_time.group(1)
#        item['release_switch_time'] = time.mktime(time.strptime(t.search(doc.html()).group(1),'%Y-%m-%d %H:%M:%S'))
        item['source'] = u'搜狐'
        author = doc('div[class = "function clear"]')
        self.author = author('div.l')('a').text()
        item['author'] = self.author
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0 and self.release_time:
            return True
        else:
            return False
