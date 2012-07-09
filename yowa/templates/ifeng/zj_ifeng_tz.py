#coding: utf-8
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'ifengtz001'
    #凤凰股吧

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div[id *= "postmessage_"]')

        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('script')
        

        content = content_node.__unicode__()

        item = ContentItem()
        

        item['title'] = self.title = doc('div.titleMs').find('strong').text()
        item['author'] = self.author = doc('div.nm01').find('strong').eq(0).text()
            
        item['content'] = self.content = content
        
        self.release_time = doc('div[class = "nm01"]').eq(0).text()
        p = re.compile(u"(20\d\d.*:\d\d)")
        item['release_time'] = self.release_time = p.search(self.release_time).group()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d %H:%M'))
                    
        item['source'] = u"凤凰网"
        author = doc('div[class = "nm01"]').eq(0).find('strong').text()
        item['author'] = author
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
