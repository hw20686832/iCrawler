#coding: utf-8

from pyquery import PyQuery

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = '21cn_xw_1'

    def extract(self):
        doc = PyQuery(self.html)
        content_node = doc('div#article_text')
        content_node.remove('div.page-box')

        item = ContentItem()
        imgs = content_node('img')
        img_all = []
        for img in imgs:
            if img.get('src').endswith('.gif'):
                continue
            else:
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                img_all.append(self.getRealURI(img.get('src')))

        item['image_urls'] = img_all
        self.title, = self.hxs.select("//div[@class='hd']/h1/text()").extract()
        self.content = content_node.__unicode__()
        item['title'] = self.title
        item['content'] = self.content
        release_time, = self.hxs.select("//div[@class='hd']//span[@class='pubTime']/text()").extract()
        item['release_time'] = release_time
        item['source'] = u"21CN娱乐"

        return item

    def isMatch(self, ):
        return len(self.title) > 0 and len(self.content) > 0
