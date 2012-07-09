#coding: utf-8
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

class Parser(Base):
    name = 'yunnan001'
    

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div#layer216')

        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('script')
        content_node.remove('div#displaypagenum')
        content_node.remove('input')
        

        content = content_node.__unicode__()

        item = ContentItem()
        

        item['title'] = self.title = doc('div#layer213').text()
            
        item['content'] = self.content = content
        
        self.release_time = doc('div#layer214').text()
        p = re.compile(u"(20\d\d.*:\d\d)")
        item['release_time'] = self.release_time = p.search(self.release_time).group()
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(self.release_time,u'%Y-%m-%d %H:%M:%S'))
                    
        item['source'] = u"云南网"
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
