#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'aoyou'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        try:
            content_node = doc('#UC_newsInfoDetail_hidCon').attr('value')
            item['content'] = self.content = content_node
        except:
            content_node = doc('input').eq(2)
            item['content'] = self.content = content_node.__unicode__()
        
        img_conten = PyQuery(content_node)
        item['image_urls'] = [self.getRealURI(img.get('src')) for img in img_conten('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('#UC_newsInfoDetail_lbl_newsTitle').text()
                  
        item['release_time'] = self.release_time = doc('#UC_newsInfoDetail_lbl_newsAuthorAndTime').text()
        item['source'] = u'遨游网'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
