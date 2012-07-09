#coding: utf-8
'''
Created on 2012-3-7

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'gaibar_xw'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('.zenwen')
        content_node.remove('#ArticleKeywordUrl')
        content_node.remove('.updown')
        content_node.remove('.pinlun')
        content_node.remove('.bot_cla')
        content_node.remove('b')
        
        item = ContentItem()
        imgs = content_node('li.content')('img')
        img_all = []
        for img in imgs:
            if".gif" in img.get('src'):
                continue
            else:  
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                img_all.append(self.getRealURI(img.get('src')))
        item['image_urls'] = img_all
                
        item['title'] = self.title = content_node('li.text1').text()
        item['content'] = self.content = content_node('li.content').__unicode__()    
        
        release_time=doc('.liuliang').text()
        ob=re.compile(u'20\d\d.*-\d?')
        release_time=ob.findall(release_time)
            
        item['release_time'] = release_time[0]
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time[0],u'%Y-%m-%d'))
        item['source'] = u"改吧"
        item['author'] = ''
        item['pic_url'] = ''
        
        self.title = item['title']
        self.content = item['content']
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False