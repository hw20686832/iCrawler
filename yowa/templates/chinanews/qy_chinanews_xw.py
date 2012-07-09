#coding=utf-8
import re

from pyquery import PyQuery

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'chinanews'

    def extract(self):
        item = ContentItem()

        doc = PyQuery(self.html)
        body_node = doc('div.left_zw')
        content_node = doc('div.left_ph')
        content_node.extend(doc('div.left_pt'))
        content_node.extend(body_node)
        content_node.remove('style')

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('#title_tex').text()
        if not item['title']:
            item['title'] = self.title = doc('h1').text()
        item['content'] = self.content = content_node.__unicode__()          
        item['release_time'] = self.release_time = doc('div[class="left-t"]').text()[:17]
        item['source'] = u'中新网'

        return item

    def isMatch(self, ):
        return len(self.title) > 0 and len(self.content) > 0
