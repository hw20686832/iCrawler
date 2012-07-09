#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image
import time

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = '41go'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.content')
        content_node('img').append('<br><br>')

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('span#lbltitle').text()
        item['content'] = self.content = doc('strong.intro').__unicode__() + content_node.__unicode__()
        item['release_time'] = self.release_time = doc('#lblcreatetime').text()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d %H:%M:%S'))
        item['source'] = u'试衣网'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
