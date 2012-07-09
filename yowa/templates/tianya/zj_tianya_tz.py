#coding: utf-8
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem
from scrapy.selector import HtmlXPathSelector

class Parser(Base):
    name = 'tianya001'
    #天涯

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.post').eq(0)

        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('script')
        item = ContentItem()
        
        imgs = content_node('img')
        image_urls = []
                    
        for img in imgs:
            if img.get('original'):
                imgs.eq(imgs.index(img)).attr["src"] = img.get('original')
                if ".gif" in img.get('src'):
                    continue
                if not img.get('src'):
                    continue
                else:
                    image_urls.append(self.getRealURI(img.get('src')))
            else:
                if ".gif" in img.get('src'):
                    continue
                if not img.get('src'):
                    continue
                else:
                    image_urls.append(self.getRealURI(img.get('src')))
        item['image_urls'] = image_urls

        content = content_node.__unicode__()

        
        

        item['title'] = self.title = doc('h1#hTitle').text()
        item['author'] = self.author = doc('div.vcard').eq(0).find('a').text()
        if not item['author']:
            item['author'] = self.author = doc('table#firstAuthor').find('a').text()
            
        item['content'] = self.content = content
        
        self.release_time = doc('div.vcard').eq(0).text()
        if not self.release_time:
            self.release_time = doc('table#firstAuthor').text()
        p = re.compile(u"(20\d\d-.*:\d\d)")
        item['release_time'] = self.release_time = p.search(self.release_time).group()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d %H:%M:%S'))
                    
        item['source'] = u"天涯"
        #item['author'] = self.hxs.select("//table[@id = 'firstAuthor']//td[@align = 'center']/a/text()").extract()[0]
        item['pic_url'] = ''

        

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
