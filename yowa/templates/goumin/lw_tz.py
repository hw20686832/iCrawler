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
    name = 'goumin_tz'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('.bc')
        
        item = ContentItem()
        imgs = content_node('.p90').eq(0)('img')
        img_all = []
        for img in imgs:
            if".gif" in img.get('src'):
                continue
            else:  
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                img_all.append(self.getRealURI(img.get('src')))
        item['image_urls'] = img_all
        
        content_node1 = doc('div[class = "wr f12 lh20"]').text()
        content_node2 = doc('div[class = "wr f14"]')
        content_node3 = doc('div[class = "f14 p90 pl10"]')
        
        release_time=content_node('.wr')('span').text()
        ob=re.compile(u'20\d\d.*\d\d')
        release_time=ob.findall(release_time)
        
        item['release_time'] = release_time[0]
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time[0],u'%Y-%m-%d %H:%M'))
        item['source'] = u"狗民网"
        item['author'] = content_node('.gray')('a').eq(0).text()
        
        item['title'] = self.title = content_node('.p90').eq(0)('.B').text()
        
        tz_content=content_node('.p90').eq(0)
        tz_content.remove('span')
        tz_content.remove('.B')
        
        content = tz_content.__unicode__()
        content = content + "<p>================</p>"
        if content_node1:
            content = content + u"<p>医师回答：</p>"
            content = content + content_node1
            content = content + "<p>-----------------</p>"
        if len(content_node2)>1:
            content = content + u"<p>最佳答案：</p>"
            content = content + content_node2.eq(1).text()
            content = content + "<p>-----------------</p>"
        if len(content_node3)>0:
            n = 0
            for cont in content_node3:
                n = content_node3.index(cont)+1
                content = content + "<p> " + str(n) +u" 楼</p>"
                content = content + content_node3.eq(content_node3.index(cont)).__unicode__()
                content = content + "<p>-----------------</p>"
        
        item['content'] = self.content = content
        item['pic_url'] = ''
        
        self.title = item['title']
        self.content = item['content']
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False