#coding: utf-8
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'hexuntz001'
    #hexun

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div[class = "txtcont"]')
        if not content_node:
            content_node = doc('div[class = "art_context"]').eq(0)
        if not content_node:
            content_node = doc('div[class = "concent"]').eq(0)
        if not content_node:
            content_node = doc('div[class = "detail_cnt"]').eq(0)
        if not content_node:
            content_node = doc('div[class = "txtmain"]').eq(0)

        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('script')
        content_node.remove('div#aside')
        content_node.remove('div#yued')
        content_node.remove('div.shareBox')
        

        content = content_node.__unicode__()

        item = ContentItem()
        

        #item['title'] = self.title = doc('div.titleMs').find('strong').text()
        self.title = doc('h1').text()
        if not self.title:
            self.title = doc('div.articleTitle').text()
        if not self.title:
            self.title = doc('div.arttitle').find('strong').text()
        item['title'] = self.title

        self.author = doc('a.owner').text()
        if not self.author:
            self.author = doc('dl.ftrmod').find('a.f06c0').text()
        if not self.author:
            if doc('div[class = "articleInfo_l"]')('a'):
                author = doc('div[class = "articleInfo_l"]')('a').text()
            else:
                author = doc('div[class = "articleInfo_l"]').text()
                a = re.compile(u'楼主(.*)发表于')
                self.author = a.match(author).group(1)
        item['author'] = self.author
            
        item['content'] = self.content = content
        
        self.release_time = doc('span[class *= "gray"]').text()
        if not self.release_time:
            self.release_time = doc('div#artInfo').text()
        if not self.release_time:
            self.release_time = doc('dl.ftrmod').find('h3').text()
        p = re.compile(u"(20\d\d.*:\d\d)")
        item['release_time'] = self.release_time = p.search(self.release_time).group()
                    
        item['source'] = u"和讯"
        
            
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
