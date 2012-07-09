#coding: utf-8
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'yahoo001'
    

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div[class = "text fixclear"]')

        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('script')
        

        

        item = ContentItem()
        
        if doc('h1').eq(1).text():
            item['title'] = self.title = doc('h1').eq(1).text()
        else:
            item['title'] = self.title = doc('h1').text()
            
        
        t = re.compile(u'(20\d\d.*:\d\d)')
        self.release_time = doc('div[class="title"]').find('span').eq(0).text()
        item['release_time'] = self.release_time = t.search(self.release_time).group()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y年%m月%d日%H:%M'))
        item['source'] = u'雅虎'
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
