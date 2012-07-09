#coding: utf-8
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'sina007'
    #暗黑3


    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div[class = "Center_main_con Zli_font3"]')
        if not content_node:
            content_node = doc('td[class = "f1413"]')
        
        content_node.remove('script')
        content_node.remove('style')
        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('input')
        
        

        item = ContentItem()
        item['title'] = self.title = doc('h3').text()
        if not self.title:
            item['title'] = self.title = doc('b').eq(0).text()
        
        
        
        self.release_time = doc('h4.li_font11').text()
        p = re.compile(u"(20.*:\d\d)")
        item['release_time'] = self.release_time = p.search(self.release_time).group()
        
        item['source'] = u"新浪"
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
                imgs.eq(imgs.index(img)).before('<br>')
                imgs.eq(imgs.index(img)).append('<br>')
                image_urls.append(self.getRealURI(img.get('src')))
        item['image_urls'] = image_urls

        content = content_node.__unicode__()
        item['content'] = self.content = content
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
