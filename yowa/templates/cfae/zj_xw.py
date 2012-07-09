#coding: utf-8

import re
import time
from pyquery import PyQuery
import Image
import string

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'zj_cfae'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('table.xm_tab')
        if not content_node:
            content_node = doc('td#zoom')
        
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
        
        self.title = doc('td.xm_logo')
        if self.title:
            self.title = self.title.remove('div.xm_xq')
            self.title = self.title.text()
        if not self.title:
            self.title = doc('h3').text()
        item['title'] = self.title
        content_node = content_node.__unicode__()
        content_node = content_node.replace('border="0"','border="1"')
        item['content'] = self.content = content_node
        deadline = self.hxs.select("//table[@class='xm_tab'][1]//tr[8]/td[4]/text()").extract()
        if len(deadline) >0:
            deadline = string.strip(deadline[0])
        dl = re.compile(u"(20\d\d-\d\d-\d\d)")
        deadline = dl.findall(deadline)
        if len(deadline) ==2 :
            item['deadline'] = deadline[1]
        item['release_time'] = ''
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time,u'%Y��%m��%d��%H:%M'))
        item['source'] = u"北京金融资产交易所"
        item['author'] = ''
        item['pic_url'] = ''
        item['city'] = u"北京"
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
