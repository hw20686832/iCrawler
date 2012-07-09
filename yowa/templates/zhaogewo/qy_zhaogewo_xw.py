#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image
import time
import re

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'zhaogewo'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node1 = doc('div.decontent_con').eq(0).find('div').eq(0)
        content_node = doc('div.decontent_con')
        
        self.content = content_node1.text() + "<p>================</p>"
        count = 0
        for con in content_node:
            if count == 0:
                count = count+1
                continue
            else:
                if not content_node('div.decontent_listbox') and count == 1:
                    self.content = self.content +  "<P>"+str(count)+u" 楼<P>"
                    self.content = self.content + content_node.eq(content_node.index(con)).__unicode__()
                    self.content = self.content + "<p>-----------------</p>"  
                    count = count+1
                else:
                    content_node2 = content_node.eq(content_node.index(con)).find('div[class = "decontent_listbox_wenzi"]').find('div').eq(1)
                    if not content_node2.text():
                        continue
                    else:
                        self.content = self.content +  "<P>"+str(count)+u" 楼<P>"
                        self.content = self.content + content_node2.__unicode__()
                        self.content = self.content + "<p>-----------------</p>"
                        count = count+1 

        item['title'] = self.title = doc('h4').text()
        item['content'] = self.content 
        p = re.compile(u'[\d]{4}-[0,1]?[\d]-[0-3]?[\d][\ ][0,1,2]?[\d]:[0-5]?[\d]:[0-5]?[\d]')
        item['release_time'] = self.release_time = p.search(doc('div.decontent_nametime').text()).group()
#        item['release_switch_time'] = time.mktime(time.strptime(self.release_time,'%Y-%m-%d %H:%M:%S'))
        item['source'] = u'找个窝'
        item['author'] = ''
        item['pic_url'] = ''
        item['image_urls'] = []

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
