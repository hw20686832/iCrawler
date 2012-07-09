#coding: utf-8
import re
import string
import time

from pyquery import PyQuery

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'tuan800_1'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.deal_content')
        item = ContentItem()
        content_image = doc('a[class = "deal_out_link"]').find('img').attr('src')
        item['image_urls'] = [content_image,]
        price = content_node('div#dealinfo')('h3')('b').text()

        content = doc('h1').text()
        
        image="<br/><br/><img src='"+content_image+"'>"
        content=content+image
        item['title'] = self.title = doc('h1').text()
        item['content'] = self.content = content
        item['price'] = price
        #item['city'] = 
        item['release_time'] = ''
        item['source'] = u'团800'
        item['author'] = ''
        item['pic_url'] = ''
        
        deadline_d = doc('div[id = "dealinfo"]').attr('info')
        deadline_d = deadline_d.split(',')
        if deadline_d:
            deadline = deadline_d[2]
            deadline = deadline[0:10]
            deadline = string.atoi(deadline)
            deadline = time.localtime(deadline)
            item['deadline'] = time.strftime('%Y-%m-%d',deadline)
        else:
            item['deadline'] = ''
        
        return item

    def isMatch(self):
        return len(self.title) > 0 and len(self.content) > 0
