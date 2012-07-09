#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'pcauto'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('#newsbody').remove('div[class = "sjkhd"]')
        if not content_node:
            content_node = doc('div[class="artText"]')

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('h1').text()
        item['content'] = self.content = content_node.__unicode__()          
        item['release_time'] = self.release_time = doc('div[class = "t0601sviewurl"]').find('span').eq(0).text()[3:]
        if not item['release_time']:
            item['release_time'] = doc('div[class="artExt smoke"]').text()[:16]
        item['source'] = u'pcauto'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
