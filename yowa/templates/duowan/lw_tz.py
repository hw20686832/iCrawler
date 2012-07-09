#coding: utf-8
'''
Created on 2012-2-14

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image
import re

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'duowan_tz'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('.t_fsz').eq(0)
        content_node.remove('#p_btn')
        content_node.remove('div.locked')
        content_node.remove('embed')
        content_node.remove('iframe')
        content_node.remove('.jammer')
        content_node.remove('span')

        if not  content_node:
            content_node=doc('td.t_f')
            content_node.remove('script')
            content_node.remove('i')
        
        item = ContentItem()
        imgs = content_node('img')
        img_all = []
        for img in imgs:
            if".gif" in img.get('src'):
                continue
            else:  
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                img_all.append(self.getRealURI(img.get('src')))
        item['image_urls'] = img_all
        
        item['title'] = self.title = doc('#thread_subject').text()
        item['content'] = self.content = content_node.__unicode__()
        
        release_time=doc('.authi')('em').eq(0).text()
        ob=re.compile(u'20\d\d.*:\d\d')
        re_time=ob.findall(release_time)
        if not re_time:
            re_time=doc('.authi')('em')('span').eq(0)
            re_time=re_time.attr('title') 
        else:
            re_time=re_time[0]
            
        item['release_time'] = re_time
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(re_time,u'%Y-%m-%d %H:%M:%S'))
        item['source'] = u"多玩论坛"
        item['author'] = doc('.authi')('a').eq(0).text()
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False