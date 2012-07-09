#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'ifeng'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('#artical_real')
        content_node.remove('span')
        content_node.remove('div.detailPic')
        content_node.remove('img[height = "7"]')
        
        imgs = content_node('img')
        image_urls = []
        for img in imgs:
            if ".gif" in img.get('src'):
                continue
            if not img.get('src'):
                continue
            else:
                imgs.eq(imgs.index(img)).before('<br>')
                imgs.eq(imgs.index(img)).append('<br><br>')
                image_urls.append(self.getRealURI(img.get('src')))
        item['image_urls'] = image_urls

        item['title'] = self.title = doc('h1').text()
        if not item['title']:
            item['title'] = self.title = doc('div#artical_topic').text()
        item['content'] = self.content = content_node.__unicode__()
        item['release_time'] = self.release_time = doc('#artical_sth')('p')('span').eq(0).text()
        item['source'] = u'凤凰网'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
