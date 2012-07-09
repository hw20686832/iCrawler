#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'pconline_xw'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div[class="art_con"]')
        
        content_node.remove('div[class = "pconline_page"]')
        content_node.remove('div[class = "pc3g"]')
        content_node.remove('div[class = "pageTips"]')
        content_node.remove('div[class = "art_nav_box mt10"]')
        content_node.remove('div[class = "art_bottom"]')

        

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('h1').text()
        if not item['title']:
            item['title'] = self.title = doc('#UC_newsInfoDetail_lbl_newsTitle').text()
        item['content'] = self.content = content_node.__unicode__()
        release_time = doc('div[class="art_con_top"]').text()
        p = re.compile(u'20\d\d-.*:\d\d')
        #item['release_time'] = self.release_time = doc('div[class="art_con_top"]').find('span').eq(0).text()
        item['release_time'] = self.release_time = p.search(release_time).group()
        item['source'] = u'pconline'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
