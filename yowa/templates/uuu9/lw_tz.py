#coding: utf-8
'''
Created on 2012-2-14

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'uuu9_tz'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('.t_msgfontfix').eq(0)
        if not content_node:
            content_node=doc('.postmessage')('form').eq(0)
        
        item = ContentItem()
        imgs = content_node('img')
        img_all = []
        for img in imgs:
            if img.get('file')==None:
                if ".gif" in img.get('src'):
                    continue
                else:
                    imgs.eq(imgs.index(img)).append('<br>')
                    imgs.eq(imgs.index(img)).before('<br>')
                    img_all.append(self.getRealURI(img.get('src')))
            else:
                if ".gif" in img.get('file'):
                    break
                else:
                    imgs.eq(imgs.index(img)).append('<br>')
                    imgs.eq(imgs.index(img)).before('<br>')
                    img_all.append(self.getRealURI(img.get('file')))
        item['image_urls'] = img_all
        
        item['title'] = self.title = doc('#threadtitle')('h1').text()
        item['content'] = self.content = content_node.__unicode__()
        release_time=doc('.authorinfo')('em').eq(0).text()
        ob=re.compile(u'20\d\d.*\d\d')
        release_time=ob.findall(release_time)
        if not release_time:
            release_time=doc('.authorinfo')('em')('span').eq(0)
            release_time=release_time.attr('title')
        else:
            release_time=release_time[0]
        item['release_time'] = release_time
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time,u'%Y-%m-%d %H:%M'))
        item['source'] = u"游久社区"
        item['author'] = doc('.postinfo')('a').eq(0).text()
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False