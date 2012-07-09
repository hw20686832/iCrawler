#coding: utf-8

from pyquery import PyQuery

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'cri_xw_1'

    def extract(self):
        doc = PyQuery(self.html)
        content_node = doc('div#ccontent')

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
        self.title, = self.hxs.select("//h1[@class='ctitle']/text()").extract()
        self.content = content_node.__unicode__()
        item['title'] = self.title
        item['content'] = self.content
        release_time_str, = self.hxs.select("//div[@class='signdate']/text()").extract()
        item['release_time'] = ' '.join(release_time_str.split()[:2])
        item['source'] = u"国际在线"

        return item

    def isMatch(self, ):
        return len(self.title) > 0 and len(self.content) > 0
