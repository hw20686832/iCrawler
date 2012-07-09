#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image
import time
import re

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'zhzyw'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.webnr')
        content_node.remove('span').remove('style')
        content_node('img').append('<br><br>')

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('h1').text()
        item['content'] = self.content = re.sub('&\w+;', '', content_node.__unicode__())
        p = re.compile(u'[\d]{4}-[0,1]?[\d]-[0-3]?[\d][\ ][0,1,2]?[\d]:[0-5]?[\d]:[0-5]?[\d]')
        item['release_time'] = self.release_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d %H:%M:%S'))
        item['source'] = u'中华中医网'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
