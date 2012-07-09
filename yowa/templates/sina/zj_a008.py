#coding: utf-8
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'sina008'
    #单机游戏


    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('table[style = "border:1px solid #D0D0D0;margin-top:5px"]').find('tr').eq(2)
        
        content_node.remove('script')
        content_node.remove('style')
        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('input')
        
        

        item = ContentItem()
        item['title'] = self.title = doc('table[style = "border:1px solid #D0D0D0;margin-top:5px"]').find('tr').eq(0).text()       
        
        item['release_time'] = ''
        
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
