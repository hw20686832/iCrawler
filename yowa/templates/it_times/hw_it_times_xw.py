#coding: utf-8
import re

from pyquery import PyQuery

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'it_times_xw_1'

    def extract(self):
        doc = PyQuery(self.html)
        content_node = doc('div.content')

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
        self.title, = self.hxs.select("//div[@class='list_main']//div[@class='docu']/h1/text()").extract()
        self.content = content_node.html()
        item['title'] = self.title
        item['content'] = self.content
        release_time_str = self.hxs.select("//div[@class='list_main']//div[@class='docu']/h2/text()").extract()[0]
        item['release_time'] = re.search(u"(20\d{2}(-\d{2}){2} \d{2}(:\d{2}){2})", release_time_str).group(0)
        item['source'] = u"IT时报"

        return item

    def isMatch(self, ):
        return len(self.title) > 0 and len(self.content) > 0
