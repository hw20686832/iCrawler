#coding: utf-8
import re
import time

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = '18023001'
    

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('table[style = "margin-top:8px"]')
        if not content_node:
            content_node = doc('div[class = "bd"]').eq(0)

        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('script')
        content_node.remove('td[colspan = "2"]')
        content_node.remove('div.like')
        content_node.remove('div.newspic')
        

        content = content_node.__unicode__()

        item = ContentItem()
        

        item['title'] = self.title = doc('td[style = "font-size:12pt;padding-top:10px"]').text()
        if not item['title']:
            item['title'] = self.title = doc('div[class = "titlex c"]').text()
        if not item['title']:
            item['title'] = self.title = doc('div.titlex').text()
            
        item['content'] = self.content = content
        
        self.release_time = doc('td[style = "border-top:1px solid #449900; padding-top:5px;"]').text()
        if not self.release_time:
            self.release_time = doc('div.info').text()
        p = re.compile(u"(20\d\d.*-\d\d)")
        item['release_time'] = self.release_time = p.search(self.release_time).group()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d'))
                    
        item['source'] = u"中国钓鱼网"
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
