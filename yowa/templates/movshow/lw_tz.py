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
    name = 'movshow_tz'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('.t_fsz')
        content_node.remove('.tip')
            
        
        item = ContentItem()
        imgs = content_node('img')
        img_all = []
        for img in imgs:
            if not img.get('zoomfile'):
                if ".gif" in img.get('src'):
                    imgs.eq(imgs.index(img)).attr["src"] = self.getRealURI(img.get('src'))
                    continue
                if ".GIF" in img.get('src'):
                    imgs.eq(imgs.index(img)).attr["src"] = self.getRealURI(img.get('src'))
                    continue
                if not img.get('src'):
                    continue
                else:
                    imgs.eq(imgs.index(img)).append('<br>')
                    imgs.eq(imgs.index(img)).before('<br>')
                    img_all.append(self.getRealURI(img.get('src')))
            else:
                if".gif" in img.get('zoomfile'):
                    imgs.eq(imgs.index(img)).attr["src"] = self.getRealURI(img.get('zoomfile'))
                else:
                    imgs.eq(imgs.index(img)).append('<br>')
                    imgs.eq(imgs.index(img)).before('<br>')
                    imgs.eq(imgs.index(img)).attr["src"] = img.get('zoomfile')
                    img_all.append(self.getRealURI(img.get('src')))
                    
        item['image_urls'] = img_all
        
        item['title'] = self.title = doc('#thread_subject').text()
        
        content = content_node.eq(0).__unicode__()
        content = content + "<p>================</p>"
        n = 0
        for cont in content_node:
            n = content_node.index(cont)+1
            if n == len(content_node):
                continue
            else:
                content = content + "<p> " + str(n) +u" 楼</p>"
                content = content + content_node.eq(content_node.index(cont)+1).__unicode__()
                content = content + "<p>-----------------</p>"
                
        content = content.replace('<dd>','')
        content = content.replace('</dd>','')
        item['content'] = self.content = content
        
        release_time=doc('.authi')('em').eq(0).text()
        ob=re.compile(u'20\d\d.*\d\d')
        release_time=ob.findall(release_time)
        if not release_time:
            release_time=doc('.authi')('span')
            release_time=release_time.attr("title")
        else:
            release_time=release_time[0]
        
        item['release_time'] = release_time
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time,u'%Y-%m-%d %H:%M:%S'))
        item['source'] = u"猫咪有约"
        item['author'] = doc('.authi')('a').eq(0).text()
        item['pic_url'] = ''
        
        self.title = item['title']
        self.content = item['content']
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False