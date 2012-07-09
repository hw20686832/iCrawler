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
    name = 'sina_tz_yx'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('.defaultpost')
        if not content_node:
            content_node = doca('table[width="660"]').remove('div') 
        
        content_node.remove('div[class = "ad_pip"]')
        item = ContentItem()
        imgs = content_node('table').eq(0)('img')
        img_all = []
        for img in imgs:
            if "gif" in img.get('src'):
                continue
            else:
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                img_all.append(self.getRealURI(img.get('src')))
        item['image_urls'] = img_all
        
        title = doc('#threadtitle')('h1').text()
        d = re.compile(u'(\[.*?\])')
        title = d.sub('',title)
        
        release_time=doc('.authorinfo')('em').eq(0).text()
        ob=re.compile(u'20\d\d.*\d\d')
        re_time=ob.findall(release_time)
        if not re_time:
            re_time=doc('.authorinfo')('em')('span').eq(0)
            re_time=re_time.attr('title') 
        else:
            re_time=re_time[0]
        
        item['title'] = self.title = title
        item['content'] = self.content = content_node('table').eq(0).__unicode__()
        item['release_time'] = re_time
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(re_time,u'%Y-%m-%d %H:%M'))
        item['source'] = u"新浪"
        item['author'] = doc('.popuserinfo')('a').eq(0).text()
        item['pic_url'] = ''
                
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False