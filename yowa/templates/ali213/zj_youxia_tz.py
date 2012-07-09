#coding: utf-8
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'ali213001'
    #游侠论坛

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('td[id *= "postmessage_"]').eq(0)
        if not content_node:
            content_node = doc('div[class="t_fsz"]')
        if not content_node:
            content_node = doc('div[class = "f_content"]')

        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('script')
        content_node.remove('div[class = "page_fenye"]')
        

        content = content_node.__unicode__()

        item = ContentItem()
        

        item['title'] = self.title = doc('h1').find('a[id = "thread_subject"]').text()
        if not item['title']:
            item['title'] = self.title = doc('div.title')('div.b')('a').text()
        
        item['author'] = self.author = doc('div[id *= "post_"]').eq(0).find('a.xw1').text()
            
        item['content'] = self.content = content
        
        item['release_time'] = self.release_time = doc('em[id *= "authorposton"]').find('span').attr('title')
        if not self.release_time:
            self.release_time = doc('em[id *= "authorposton"]').eq(0).text()
        if not self.release_time:
            self.release_time = doc('ul.cont')('li').eq(3).text()
        p = re.compile(u"(20\d\d.*:\d\d)")
        item['release_time'] = self.release_time = p.search(self.release_time).group()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d %H:%M:%S'))
                    
        item['source'] = u"游侠论坛"
        item['author'] = ''
        item['pic_url'] = ''

        imgs = content_node('img')
        image_urls = []
        for img in imgs:
            if ".gif" in img.get('src'):
                if not img.get('file'):
                    continue
                else:
                    image_urls.append(self.getRealURI(img.get('file')))
            else:
                image_urls.append(self.getRealURI(img.get('src')))
        item['image_urls'] = image_urls

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
