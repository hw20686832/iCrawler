#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = '163cj'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('#endText')
        content_node.remove('span')

#        content_node.remove('table')
        content_node.remove('.gg200x300')
        content_node.remove('.clearfix').remove('iframe')
        content_node('img').append('<br>')

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('h1').text()
        self.content = content = re.sub('&\w+;', '', content_node.__unicode__())
        content = content.replace('<u>','')
        item['content'] = content.replace('<u/>','')
        item['release_time'] = self.release_time = doc('span').filter('.info').text()[0:19]
        item['source'] = u'网易'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
