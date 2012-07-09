#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'astron'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('tr[valign="top"]')
        if not content_node:
            content_node = doc('div.a_content')
        content_node.remove('style')

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('td[class="bt_title"]').text()
        if not self.title:
            item['title'] = self.title = doc('h2.a_title').text()
        item['content'] = self.content = content_node.__unicode__()
        t = re.compile(u"(20\d\d-\d\d-\d\d)")
        self.release_time = doc('td[height="20"]').text()
        if not self.release_time:
            self.release_time = doc('div.a_legend').text()
        item['release_time'] = self.release_time = t.search(self.release_time).group()
        item['source'] = u'天文科普网'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
