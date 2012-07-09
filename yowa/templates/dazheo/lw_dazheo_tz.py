#coding: utf-8
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'dazheo_tz'
    #����

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.t_fsz').eq(0)
        

        content = content_node.__unicode__()

        item = ContentItem()
        item['title'] = self.title = doc('h1.ts')('a#thread_subject').text()
        
        item['content'] = self.content = content
        self.release_time = doc('div.authi')('em').eq(0).text()
        p = re.compile(u"(20.*:\d\d)")
        self.release_time = p.findall(self.release_time)
            
        item['release_time'] = self.release_time
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d %H:%M:%S'))
            
        item['source'] = u"打折喔"
        item['author'] = ''
        item['pic_url'] = ''

        imgs = content_node('img')
        image_urls = []
        for img in imgs:
            if ".gif" in img.get('file'):
                continue
            if not img.get('file'):
                continue
            else:
                image_urls.append(self.getRealURI(img.get('file')))
        item['image_urls'] = image_urls

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
