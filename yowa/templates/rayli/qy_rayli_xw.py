#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image
import time
import re

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'rayli'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.clear.clean')
        content_node.remove('span')
        content_node('img').append('<br><br>')

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('h2').text()
        if not item['title']:
            item['title'] = self.title = doc('h1.dcyfsh1').text()
        item['content'] = self.content = re.sub('&\w+;', '', content_node.__unicode__())
        p = re.compile(u"(20\d\d.*\d\d:\d\d)")
        item['release_time'] = self.release_time = p.search(doc('div[class = "w645 txtCenter grey89 marginb25"]').text()).group()
#        item['release_switch_time'] = self.release_switch_time = time.time()
        item['source'] = u'瑞丽'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
