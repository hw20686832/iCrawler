#coding: utf-8
'''
Created on 2012-2-11

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = '17173_tz'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('.firstTopic')('div')
        content_node.remove('script')
        content_node.remove('.rate')
        content_node.remove('.affixContent')
        content_node.remove('.thread_gold')
        
        
        item = ContentItem()
        imgs = content_node('.p14')('img')
        img_all = []
        for img in imgs:
            if".gif" in img.get('src'):
                continue
            else:  
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                img_all.append(self.getRealURI(img.get('src')))
        item['image_urls'] = img_all
        
        item['title'] = self.title = doc('#thread_title').text()
        content = content_node('.p14').__unicode__()
        content = PyQuery(content)
        del_style = content('div')
        for d in del_style:
            if d.get('style'):
                del_style.eq(del_style.index(d)).attr['style'] = ''
                
        content.remove('dl.rate_list')
        content.remove('span[style = "font-size:12px"]')
        content.remove('dl.rate')
        item['content'] = self.content = content.__unicode__()
        
        release_time=doc('.firstTopic')('.postTime').text()
        ob=re.compile(u'20\d\d.*\d\d')
        release_time=ob.findall(release_time)
        
        item['release_time'] = release_time[0]
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time[0],u'%Y-%m-%d %H:%M:%S'))
        item['source'] = u"17173论坛"
        item['author'] = doc('.th1').eq(0).text()
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False