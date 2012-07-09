#coding: utf-8
import re

from pyquery import PyQuery

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'ifengbk001'
    #凤凰博客

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div#blog_article_content')

        content = content_node.outerHtml()
        cpl = re.compile('<img.*?src=".*?"', re.I)
        content = re.sub('%', '%%', content)
        content_doc = PyQuery(content)
        content_doc('img').attr('src', '%s')

        item = ContentItem()
        item['title'] = self.title = doc('div.blog_main_left_content').find('h3').text()
        item['author'] = self.author = doc('div#common_person_blogtitle')('div#title01')('a').text()

        item['content'] = self.content = content_doc.outerHtml()

        self.release_time = doc('div.blog_main_time').find('p').text().strip()
        item['release_time'] = self.release_time

        item['source'] = u"凤凰网"
        item['pic_url'] = ''

        item['image_urls'] = [img.get('src') for img in content_node('img')]

        return item

    def isMatch(self, ):
        return len(self.title) > 0 and len(self.content) > 0
