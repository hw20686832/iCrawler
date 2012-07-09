#coding: utf-8
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'gamersky001'
    

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div#pzoom')

        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('script')

        

        content = content_node.__unicode__()

        item = ContentItem()
        

        item['title'] = self.title = doc('span.STYLE3').text()
            
        item['content'] = self.content = content
        
        self.release_time = doc('font[class = "b12"][color = "#0123d0"]').eq(0).text()
        p = re.compile(u"(\d\d-\d\d-\d\d.*:\d\d)")
        item['release_time'] = self.release_time = "20"+p.search(self.release_time).group()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d %H:%M'))
                    
        item['source'] = u"内蒙古新闻网"
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
