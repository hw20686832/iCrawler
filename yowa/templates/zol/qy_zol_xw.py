#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'zol'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('#cotent_idd')
        content_node.remove('span')
        content_node.remove('div.Al_120')
        content_node.remove('table[style="BORDER-BOTTOM: medium none; BORDER-LEFT: medium none; BORDER-COLLAPSE: collapse; BORDER-TOP: medium none; BORDER-RIGHT: medium none"]')
        content_node.remove('table[style="border-bottom: medium none; border-left: medium none; border-collapse: collapse; border-top: medium none; border-right: medium none"]')
            
        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('h1').text()
        item['content'] = self.content = content_node.__unicode__()
        self.release_time = doc('div[class = "tit_t1 clearfix"]').text()
        if not self.release_time:
            self.release_time = doc('div[class = "tit_t1 clearfix tc"]').text()
        p = re.compile(u"(20\d\d年\d\d月.*\d\d:\d\d)")
        item['release_time'] = self.release_time = p.search(self.release_time).group()
        #item['source'] = self.source = doc('a').filter('.hei12').text()
        item['source'] = u'中关村在线'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
