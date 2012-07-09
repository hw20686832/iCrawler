#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image
import time

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'sportica'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.edit')
        if not content_node:
            content_node = doc('div.content.112843')
        content_node.remove('span')
        content_node.remove('font')
        content_node.remove('iframe')
        content_node('img').append('<br>')

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('h1').text()
        if not item['title']:
            item['title'] = self.title = doc('a.arTitle').text()
        item['content'] = self.content = re.sub('&\w+;', '', content_node.__unicode__())
        p = re.compile(u'[\d]{4}-[0,1]?[\d]-[0-3]?[\d]')
        pp = re.compile(u'[\d]{4}-[0,1]?[\d]-[0-3]?[\d][\ ][0,1,2]?[\d]:[0-5]?[\d]:[0-5]?[\d]')
        item['release_time'] = self.release_time = p.search(doc('div.infos').text()).group()
        if not item['release_time']:
            item['release_time'] = self.release_time = pp.search(doc('#arInfo').text()).group()
#        try:
#            item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d'))
#        except:
#            item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d %H:%M:%S'))
        item['source'] = u'美食杰'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
