#coding: utf-8
import re

from pyquery import PyQuery

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'dyhjw_tz01'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.t_msgfontfix').eq(0).find('table').find('td[class="t_msgfont"]')
        content_node.remove('div#ad_thread3_0')
        content_node.remove('div#ad_thread4_0')

        content = content_node.html()

        item = ContentItem()
        item['title'] = self.title = doc('h1').remove('a').text()
        item['content'] = self.content = content
        time_tag = doc('div.authorinfo').eq(0).find('em').text()
        self.release_time = re.search(r'20\d{2}-.*-.* \d{2}:\d{2}', time_tag).group()
        item['release_time'] = self.release_time
        item['source'] = u"第一黄金网"
        item['author'] = doc('div.popuserinfo').eq(0).find('a').text()
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
