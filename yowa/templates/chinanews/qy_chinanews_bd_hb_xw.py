#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'chinanews_hb'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('tr[bordercolor="#D9E6F7"]').eq(5)
        if not content_node:
            content_node = doc('table[width="98%"]').eq(0)
        content_node.remove('style')

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('tr[bordercolor="#D9E6F7"]').eq(1).text()
        if not item['title']:
            item['title'] = self.title = doc('span[class="STYLE4"]').text()
        item['content'] = self.content = content_node.__unicode__()
        try:
            item['release_time'] = self.release_time = doc('tr[bordercolor="#D9E6F7"]').eq(3).text()[:20]
        except:
            item['release_time'] = self.release_time = doc('table[width="98%"]').eq(0).find('td').eq(1).text()[:20]
        item['source'] = u'湖北新闻网'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
