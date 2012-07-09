#coding: utf-8
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'hexun001'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.txtcont')
        if not content_node:
            content_node = doc('div.art_context')
        if not content_node:
            content_node = doc('div.concent')
        if not content_node:
            content_node = doc('div.detail_cnt')
            
        content_node.remove('script')
        content_node.remove('style')
        content_node.remove('iframe')
        content_node.remove('div#aside')
        content_node.remove('div#yued')
        content_node.remove('div.shareBox')

        content_node = content_node + doc('div.mz_decl')
        content = content_node.__unicode__()

        item = ContentItem()
        item['title'] = self.title = doc('h1').text()
        if item['title'] == None:
            item['title'] = self.title = doc('div.articleTitle').text()
        
        item['content'] = self.content = content
        
        self.release_time = doc('span[class *= "gray"]').text()
        if not self.release_time:
            self.release_time = doc('div[id = "artInfo"]').text()
        p = re.compile(u"(20.*:\d\d)")
        item['release_time'] = self.release_time = p.search(self.release_time).group()
        if item['release_time'] ==None:
            self.release_time = doc('div[id = "artInfo"]').text()
            p = re.compile(u"(.*)��Դ")
            item['release_time'] = self.release_time = p.search(self.release_time).group()
        
        item['source'] = u"和讯"
        item['author'] = ''
        item['pic_url'] = ''

        imgs = content_node('img')
        image_urls = []
        for img in imgs:
            if not img.get('src'):
                continue
            elif ".gif" in img.get('src'):
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
