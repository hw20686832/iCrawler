#coding: utf-8
import re

from pyquery import PyQuery

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = '7m_xw_1'

    def extract(self):
        doc = PyQuery(self.html)
        content_node = doc('div.ny_zw')('div.zw')

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
        self.title = doc('div.ny_zw')('div.zw_bt')('p.ba').text()
        self.content = content_node.html()
        item['title'] = self.title
        item['content'] = self.content
        release_time_str = doc('div.ny_zw')('div.zw_bt')('p.bb').text()
        item['release_time'] = re.search(u"(20\d{2}年\d{2}月\d{2}日)", release_time_str).group(0)
        item['source'] = u"7M"

        return item

    def isMatch(self, ):
        return len(self.title) > 0 and len(self.content) > 0
