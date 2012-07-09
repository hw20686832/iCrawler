#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image
import re

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'pcpop'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div[class="cotent1"]')
        if not content_node:
            content_node = doc('div#contentDiv')
        content_node.remove('style')

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('h2').eq(0).text()
        if not item['title']:
            item['title'] = self.title = doc('h1').text()
        item['content'] = self.content = content_node.__unicode__()
        self.release_time = doc('div[class = "title"]').text()
        if not self.release_time:
            self.release_time = doc('div[class = "otb14"]').text()
        p = re.compile(u'[\d]{4}年[0,1]?[\d]月[0-3]?[\d]日[\   ][0,1,2]?[\d]:[0-5]?[\d]')
        item['release_time'] = self.release_time = p.search(doc('div[class="title"]').text()).group()
        
        item['source'] = u'泡泡网'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
