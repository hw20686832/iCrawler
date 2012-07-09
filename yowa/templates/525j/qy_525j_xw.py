#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image
import time
import re

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = '525j'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node1 = doc('div.question-content')
        if not content_node1.text():
            content_node1 = doc('h4.wr').text()
        else:
            content_node1 = content_node1.html()
        content_node2 = doc('div.answer-content')
        content_node2 = content_node2.html()
        
        pre1 = re.compile(u'<pre>')
        pre2 = re.compile(u'</pre>')
        pre3 = re.compile(u'<pre/>')
        
        content_node1 = pre1.sub('',content_node1)
        content_node2 = pre1.sub('',content_node2)
        content_node1 = pre2.sub('',content_node1)
        content_node2 = pre2.sub('',content_node2)
        content_node1 = pre3.sub('',content_node1)
        content_node2 = pre3.sub('',content_node2)
                
        self.content = "<p>Question:</p>" + content_node1 + "<p>================</p>" + "<p>Answer:</p>" + content_node2

        item['image_urls'] = []
        item['title'] = self.title = doc('h4.wr').text()
        item['content'] = self.content
        p = re.compile(u'[\d]{4}-[0,1]?[\d]-[0-3]?[\d][\ ][0,1,2]?[\d]:[0-5]?[\d]')
        item['release_time'] = self.release_time = p.search(doc('span.deadline').text()).group()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d %H:%M'))
        item['source'] = u'我爱我家知道网'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
