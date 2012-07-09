#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'autohome'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div[class = "articlewrap"]').find('div').eq(1)
        
        content_node.remove('embed')
        content_node.remove('iframe')
        content_node.remove('script')

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('div[class = "articlewrap"]').find('h1').text()
        item['content'] = self.content = content_node.__unicode__()
        self.release_time = doc('#articleinfo').text()
        p = re.compile(u"(20\d\d.*\d\d:\d\d)")
        item['release_time'] = self.release_time = p.search(self.release_time).group()
        item['source'] = u'汽车之家'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
