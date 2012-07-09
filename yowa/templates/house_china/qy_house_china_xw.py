#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image
import time
import re

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'house_china'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('#p_content').remove('div.page_a').remove('style').remove('div.clear').remove('div.xqtj_row')
        content_node.remove('span').remove('font')
        content_node('img').append('<br><br>')

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('h2').text()
        item['content'] = self.content = re.sub('&\w+;', '', content_node.__unicode__())
        p = re.compile(u'[\d]{4}-[0,1]?[\d]-[0-3]?[\d]')
        item['release_time'] = self.release_time = p.search(doc('h2').text()).group()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d'))
        item['source'] = u'地产中国网'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
