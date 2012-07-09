#coding: utf-8
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'tgbus001'
    

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div[class = "text"]')
        if not content_node:
            content_node = doc('div[class = "ct f14 fx"]')
        if not content_node:
            content_node = doc('div[class = "rk_content"]')
        content_node.remove('p.contentpager')
        content_node.remove('iframe')
        content_node.remove('p[class = "hide acdata"]')
        content_node.remove('embed')
        content_node.remove('script')
        content_node.remove('div[class = "ads2 fx fc t10"]')
        content_node.remove('div[class = "hide kcdata"]')
        content_node.remove('div[class = "pager t10"]')
        content_node.remove('div[class = "share fc fx t20"]')
        content_node.remove('div[class = "feel fc fx t20"]')
        content_node.remove('div[class = "Push"]')
        content_node.remove('div[class = "correlative fc fx t20"]')
        content_node.remove('div[class = "comment"]')
        content_node.remove('div[class = "appe fr fx"]')
        content_node.remove('div[class = "fc t10"]')
        content_node.remove('p[style = "text-align: center"]')
        content_node.remove('p[style = "TEXT-ALIGN: center"]')
        content_node.remove('select')
        
        

        content = content_node.__unicode__()

        item = ContentItem()
        

        item['title'] = self.title = doc('h1').text()
            
        item['content'] = self.content = content
        
        #p = re.compile(u"(20\d\d.*:\d\d)")
        #item['release_time'] = self.release_time = p.search(self.release_time).group()
        item['release_time'] = self.release_time = doc('li.d').text()
        if not item['release_time']:
            p = re.compile(u"(20\d\d年\d\d月\d\d日)")
            self.release_time = doc('div.rk_copyright').text()
            item['release_time'] = self.release_time = p.search(self.release_time).group()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y年%m月%d日%H:%M'))
                    
        item['source'] = u"电玩巴士"
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
