#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image
import time
import re

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = '39'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('#contentText')
        content_node.remove('div[class="hzh_botleft"]')
        content_node.remove('p[class="jumpto"]')
        content_node.remove('span').remove('style')
        content_node.remove('iframe')
        content_node('img').append('<br><br>')
        if not content_node:
            content_node=doc('.wrap_c').eq(0)
            content_node.remove('.in_box1_c')
        if not content_node:
            content_node=doc('td.newscontent')
        if not content_node:
            content_node=doc('div.article')
        
        imgs = content_node('img')
        image_urls = []
        for img in imgs:
            if ".gif" in img.get('src'):
                continue
            if ".GIF" in img.get('src'):
                continue
            if not img.get('src'):
                continue
            else:
                image_urls.append(self.getRealURI(img.get('src')))
        item['image_urls'] = image_urls
        item['title'] = self.title = doc('h1').text()
        if not item['title']:
            item['title'] = self.title = doc('span.newstitle').text()
            
        item['content'] = self.content = content_node.__unicode__()
        p = re.compile(u'20\d\d.*-\d?')
        self.release_time = doc('div[class="info"]').text()
        if not self.release_time:
            self.release_time = doc('div.date').text()
        if not self.release_time:
            self.release_time = doc('font[color="737373"]')
            if self.release_time:
                p = re.compile(u'20\d\d.*\d日')
                self.release_time = p.findall(self.release_time)
                self.release_time = self.release_time[0]
        else:
            self.release_time = p.findall(self.release_time)
            self.release_time = self.release_time[0]            
        item['release_time'] = self.release_time
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d'))
        item['source'] = u'39健康网'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
