#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'huanqiu'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('#text')
        if not content_node:
            content_node = doc('div.text')
        content_node.remove('style')
        content_node.remove('div.contentpage')
        content_node.remove('p.onext')
        content_node.remove('div.page')
        content_node.remove('p.pictext')

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('h1').text()
        item['content'] = self.content = content_node.__unicode__()
        item['release_time'] = self.release_time = doc('#get_date').text()
        if not item['release_time']:
            item['release_time'] = self.release_time = doc('li.time').text()
        item['source'] = u'环球网'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
