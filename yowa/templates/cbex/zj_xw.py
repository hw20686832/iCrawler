#coding: utf-8

import re
import time
from pyquery import PyQuery
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import XmlXPathSelector
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'zj_cbex'

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
        
        self.title = doc('td.xm_logo').text()
        if self.title:
            self.title = self.title.replace(u'—> 我对此项目感兴趣','')
        if not self.title:
            self.title = doc('h3').text()
        item['title'] = self.title
        content_node = content_node.__unicode__()
        content_node = content_node.replace('border="0"','border="1"')
        item['content'] = self.content = content_node
        deadline = self.hxs.select("//table[@class='xm_tab'][1]//tr[4]/td[@class = 'xmtd2'][2]/text()").extract()
        if len(deadline) >0:
            item['deadline'] = deadline[0] 
#        item['content'] = ''
        item['release_time'] = ''
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time,u'%Y��%m��%d��%H:%M'))
        item['source'] = u"北京产权交易所"
        item['author'] = ''
        item['pic_url'] = ''
        item['city'] = u"北京"
        
        return item

    def isMatch(self, ):
        if len(self.title) and len(self.content)> 0:
            return True
        else:
            return False
