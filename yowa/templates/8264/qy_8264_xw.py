#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = '8264'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div[class = "newstext"]')

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('div[class = "newstitle"]').text()
        item['content'] = self.content = content_node.__unicode__()
        try:
            self.release_time = doc('div[class = "newstitlecon"]').text().decode('gb18030')
        except:
            self.release_time = doc('div[class = "newstitlecon"]').text()
        
        p = re.compile(u"(20\d\d.*\d\d:\d\d)")            
        item['release_time'] = self.release_time = p.search(self.release_time).group()
        item['source'] = u'户外资料网'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
