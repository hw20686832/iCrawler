#coding: utf-8
import re
import time

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'youxia001'
    #游侠

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div#Content')
        if not content_node :
            content_node = doc('div.f_content')
        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('div.pagination')
        content_node.remove('script')
        content_node.remove('div[class = "page_fenye"]')
        

        content = content_node.__unicode__()

        item = ContentItem()
        
        if  doc('h1.cl_title'):
            item['title'] = self.title = doc('div.title').find('a').eq(0).text()
        else :
            item['title'] = self.title = doc('h1').eq(0).text()
            
        item['content'] = self.content = content
        
        self.release_time = doc('div.new_sl').text()
        p = re.compile(u"(20\d\d.*:\d\d)")
        item['release_time'] = self.release_time = p.search(self.release_time).group()
        if not item['release_time']:
            self.release_time = doc('ul.cont').text()
            item['release_time'] = self.release_time = p.search(self.release_time).group()
                    
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d %H:%M:%S'))
        item['source'] = u"游侠网"
        item['author'] = ''
        item['pic_url'] = ''

        imgs = content_node('img')
        image_urls = []
        for img in imgs:
            if ".gif" in img.get('src'):
                continue
            if not img.get('src'):
                continue
            else:
                image_urls.append(self.getRealURI(img.get('src')))
        item['image_urls'] = image_urls

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
