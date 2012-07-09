#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'xcar'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div[class = "artText"]')
        if not content_node:
            content_node = doc('div#newsbody')
        content_node.remove('div.sjkhd')
        content_node.remove('p[style = "padding: 0px 0pt 0px 29px;font-size:12px;"]')
        content_node.remove('div[class = "t0601_xwd_xj1"]')
        content_node.remove('p[class = "t0601_xuauk"]')
        content_node.remove('p[style = "font:normal 12px/12px normal;padding:4px 0;color:#999;text-align:center;"]')
        content_node.remove('p[class = "t_0915_ipage"]')
        content_node.remove('script')
        content_node.remove('iframe')
        content_node.remove('span.t0302_menu')
        
        imgs = content_node('img')
        image_urls = []
        for img in imgs:
            if ".gif" in img.get('src'):
                continue
            if not img.get('src'):
                continue
            else:
                imgs.eq(imgs.index(img)).before('<br>')
                image_urls.append(self.getRealURI(img.get('src')))
        item['image_urls'] = image_urls
        
        item['title'] = self.title = doc('h1').text()
        item['content'] = self.content = content_node.__unicode__()          
        item['release_time'] = self.release_time = doc('div[class = "artExt smoke"]').find('span').eq(0).text()
        if not item['release_time']:
            self.release_time = doc('div.t0601sviewurl').text()
            t = re.compile(u'20\d\d.*:\d\d')
            self.release_time = t.search(self.release_time).group()
            item['release_time'] = self.release_time
        
            
        item['source'] = u'xcar'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
