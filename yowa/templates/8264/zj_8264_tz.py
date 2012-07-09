#coding: utf-8
import re
import time

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = '8264tz001'
    #驴友论坛

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('td[id *= "postmessage_"]').eq(0)

        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('script')
        content_node.remove('div.tatt')
        content_node.remove('span.wdl')
        item = ContentItem()
        
        imgs = content_node('img')
        image_urls = []
        for img in imgs:
            if img.get('file'):
                imgs.eq(imgs.index(img)).attr["src"] = img.get('file')
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

        
        

        item['title'] = self.title = doc('a[id = "thread_subject"]').text()
        
        item['author'] = self.author = doc('div[id *= "post_"]').eq(0).find('a.xw1').text()
            
        item['content'] = self.content = content
        
        item['release_time'] = self.release_time = doc('em[id *= "authorposton"]').find('span').attr('title')
        if not item['release_time']:
            self.release_time = doc('em[id *= "authorposton"]').eq(0).text()
            p = re.compile(u"(20\d\d.*:\d\d)")
            item['release_time'] = self.release_time = p.search(self.release_time).group()
                    
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d %H:%M'))
        item['source'] = u"驴友论坛"
        item['author'] = ''
        item['pic_url'] = ''

        

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
