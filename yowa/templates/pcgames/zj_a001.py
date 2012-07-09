#coding: utf-8
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'pcgames001'
    

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div[class = "artArea"]').eq(1)
        content_node.remove('div[style = "padding:10px 0;text-align:center"]')

        content = content_node.__unicode__()

        item = ContentItem()
        

        item['title'] = self.title = doc('div.artCon').find('h1').text()
            
        item['content'] = self.content = content
        
        time_s1 = '%Y年%m月%d日'
        time_s2 = '%Y-%m-%d %H:%M'
        self.release_time = doc('p[class = "info"]').text()
        p = re.compile(u"(20\d\d.*:\d\d)")
        time_s = time_s2
        if not self.release_time:
            self.release_time = doc('p[class = "info"]').text()
            p = re.compile(u"(20\d\d年\d\d月\d\d日)")
            time_s = time_s1
        item['release_time'] = self.release_time = p.search(self.release_time).group()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,time_s))
                    
        item['source'] = u"太平洋游戏网"
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
