#coding: utf-8
'''
Created on 2012-2-13

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'ngacn_tz'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('#post1strow0')
        content_node.remove('.x')
        
        item = ContentItem()
        img = '\[img\](.*?)\[/img\]'
        ob = re.compile(img)
        imgs = ob.findall(content_node.__unicode__())
        img_all = []
        for im in imgs:
            if '.gif' in im:
                continue
            else:
                img_all.append("http://img.ngacn.cc/attachments/"+im)
        item['image_urls'] = img_all
        
        title=content_node('#postsubject0').text()
        title = title.encode('utf-8')
        title = title.replace('» ','')
        
        item['title'] = self.title = title
        item['content'] = self.content = content_node('#postcontent0').__unicode__()
        release_time=content_node('#postdate0').text()
        item['release_time'] = release_time
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time,u'%Y-%m-%d %H:%M'))
        item['source'] = u"NGA"
        item['author'] = content_node('#postauthor0').text()
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False