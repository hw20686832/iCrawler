#coding: utf-8

import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector
from yowa.items import ContentItem

class Parser(Base):
    name = 'zj_cnstock'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        
        if not doc('div[id *= "doc_"]'):
            content_node = doc('div[class = "fnomal"]')
        else:
            content_node = doc('div[id *= "doc_"]').eq(0)
            content_node.removeAttr('style')
            content_node.remove('a[href *= "javascript:goPage"]')
        
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
        
        self.title = doc('h1').text()
        if not self.title:
            self.title = doc('div.newstitle').text()
        item['title'] = self.title
        content_node = content_node.__unicode__()
        content_node = content_node.replace(u'<p>　　</p>','')
        item['content'] = self.content = content_node
        release_time=doc('div.NewProperty').text()
        r = re.compile(u"(20\d\d.*\d\d:\d\d)")
        self.release_time = r.search(release_time).group()
        item['release_time'] = self.release_time
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time,u'%Y��%m��%d��%H:%M'))
        item['source'] = u"中国证券网"
        item['author'] = ''
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
