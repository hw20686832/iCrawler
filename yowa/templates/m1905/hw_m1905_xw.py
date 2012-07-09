#coding: utf-8
import re

from pyquery import PyQuery

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'm1905_xw_1'

    def extract(self):
        doc = PyQuery(self.html)
        content_node = doc('table.content_text')

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
        self.title = doc('h1.font01.fn.ta_c.f24').text()
        self.content = content_node.html()
        item['title'] = self.title
        item['content'] = self.content
        release_time_str, = self.hxs.select("//div[@class='newsmain']//div[@class='info g6e_f']/text()").extract()
        item['release_time'] = re.search(r"(20\d{2}(-\d{2}){2} \d{2}(:\d{2}){2})", release_time_str).group(0)
        item['source'] = u"M1905电影网"

        return item

    def isMatch(self, ):
        return len(self.title) > 0 and len(self.content) > 0
