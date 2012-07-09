#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'dbw'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div[class="f14px textleft clear"]')
        content_node.remove('style')

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('div[class="padding5"]').find('b').text()
        item['content'] = self.content = content_node.__unicode__()
        item['release_time'] = self.release_time = doc('div[class="blank10px"]').eq(1).text()[79:99]
        item['source'] = u'东北网'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
