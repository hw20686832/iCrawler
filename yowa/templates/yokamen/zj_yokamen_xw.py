#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image
import time

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'yokamen'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.contentbd')
        if not content_node:
            content_node = doc('div.textCon')
        content_node.remove('span')
        content_node.remove('font')
        content_node('img').append('<br>')

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('h1').text()
        item['content'] = self.content = doc('div.contdes').__unicode__() + re.sub('&\w+;', '', content_node.__unicode__())
        p = re.compile(u'[\d]{4}-[0,1]?[\d]-[0-3]?[\d][\ ][0,1,2]?[\d]:[0-5]?[\d]')
        release_time = doc('div.conms').text()
        if not release_time:
            release_time = doc('div.time2').text()
        item['release_time'] = self.release_time = p.search(release_time).group()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d %H:%M'))
        item['source'] = u'YOKA时尚网'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
