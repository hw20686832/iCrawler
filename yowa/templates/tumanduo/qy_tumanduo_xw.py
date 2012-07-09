#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image
import time
import re

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'tumanduo'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div[style = "padding:5px 15px;line-height:20px;"]')
        count = 0
        for con in content_node:
            if count == 0:
                self.content = content_node.eq(content_node.index(con)).__unicode__() + "<p>================</p>"
                count = 1;
            else:
                self.content = self.content +  "<P>"+str(count)+" 楼<P>" 
                self.content = self.content +content_node.eq(content_node.index(con)).__unicode__() + "<p>-----------------</p>"
                count = count +1
        
        if not content_node:
            content_node = doc('div.Notop')
            content_node.remove('div[style = "padding:15px 80px"]')
            content_node.remove('div.next')
            content_node.remove('div.page')
            con_p = content_node('p')
            for p in con_p:
                if con_p.eq(con_p.index(p)).text():
                    con_p.eq(con_p.index(p)).wrap('<div></div>')
            self.content = content_node.__unicode__()
            
            p1 = re.compile(u'<p.*?>')
            self.content = p1.sub('',self.content)
            p2 = re.compile(u'<\/p>')
            self.content = p2.sub('',self.content)
        
        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('h1').text()
        if not item['title']:
            item['title'] = self.title = doc('div.Title1').eq(0).find('p').text()
        item['content'] = self.content
        p = re.compile(u'[\d]{4}-[0,1]?[\d]-[0-3]?[\d][\ ][0,1,2]?[\d]:[0-5]?[\d]')
        item['release_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#        item['release_switch_time'] = int(time.time())
        item['source'] = u'装修图满多'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
