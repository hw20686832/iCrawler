#coding: utf-8
import re
import time

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'zhongyi'
    #中医


    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div#artCon')
        
        content_node.remove('script')
        content_node.remove('style')
        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('input')
        content_node('p').find('a[target="_blank"]').remove()
        content_node.remove('span[style="color: #ff0000"]')
        content_node.remove('span[style="color: #000000"]')
        
        
        
        

        item = ContentItem()
        item['title'] = self.title = doc('h1').text()
        
        release_time = doc('div#artInfo').text()
        p = re.compile(u"(20\d\d.*\d\d:\d\d)")
        item['release_time'] = self.release_time = p.search(release_time).group()
#        item['release_switch_time'] = time.time()
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
