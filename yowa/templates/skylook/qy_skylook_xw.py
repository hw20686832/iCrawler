#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'skylook'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('#artibody').remove('p[class="page"]')
        if not content_node:
            content_node = doc('div[class="page_txt"]').find('table')
        content_node.remove('style')

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        content = content_node.__unicode__()


        item['title'] = self.title = doc('b[class="font14px"]').text()
        item['content'] = self.content = content
        t = doc('td[width="570"]').eq(0).text()
        b = re.compile(u"(20\d\d年\d\d月.*:\d\d)")
        item['release_time'] = b.search(t).group()
        item['source'] = u'星友空间站'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
