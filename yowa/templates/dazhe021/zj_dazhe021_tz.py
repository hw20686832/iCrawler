#coding: utf-8
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'dazhe_zj'
    #����

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('td[class = "t_f"]')
        

        content = content_node.__unicode__()

        item = ContentItem()
        item['title'] = self.title = doc('h1[class = "ts"]').find('a[id = "thread_subject"]').text()
        
        item['content'] = self.content = content
        self.release_time = doc('div[class = "authi"]').find('em').text()
        p = re.compile(u"(20.*:\d\d)")
        self.release_time = p.findall(self.release_time)
        if not self.release_time:
            self.release_time = doc('div[class = "authi"]')('em')('span').attr('title')
        else:
            self.release_time = self.release_time[0]
            
        item['release_time'] = self.release_time
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d %H:%M:%S'))
            
        item['source'] = u"上海打折网"
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
