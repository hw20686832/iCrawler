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
    name = 'tgbus_tz'

    def extract(self):
        item = ContentItem()
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node=doc('div.t_msgfontfix')('table').eq(0)
        if not content_node:
            content_node=doc('div.pollchart')
        if not content_node:
            content_node=doc('div.special_reward')
        if not content_node:
            content_node = doc('div.t_fsz').eq(0)
            content_node.remove('div.a_pr')

        imgs=content_node('img')
        img_all=[]
        for img in imgs:
            if '.gif' in img.get('src'):
                continue
            else:
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                img_all.append(self.getRealURI(img.get('src')))        
        item['image_urls'] = img_all
        title=doc('#threadtitle')
        title.remove('a')
        title = title.text()
        if not title:
            title = doc('a#thread_subject').text()

        release_time=doc('div.authorinfo')('em').eq(0).text()
        if not release_time:
            release_time = doc('i.pstatus').text()
        if not release_time:
            release_time  = doc('div.authi').text()
        ob=re.compile(u'20\d\d.*?:\d\d')
        re_time=ob.findall(release_time)
        if not re_time:
            release_time=doc('div.authorinfo')('em')('span').eq(0)
            re_time=release_time.attr('title')
            item['release_time'] = self.release_time = re_time
        else:
            item['release_time'] = self.release_time = re_time[0]
        item['title'] = self.title = title
        content_node.remove('i.pstatus')
        item['content'] = self.content = content_node.__unicode__()
        item['source'] = u"电玩巴士"
        item['author'] = doc('div.postinfo')('a').eq(0).text()
        if not item['author']:
            author = doc('div[class = "rk_copyright"]').text()
            t = re.compile(u'作者：(.*)来源')
            if not author:
                item['author'] = doc('a[class = "xw1"]').eq(0).text()
            else:
                item['author'] = author = t.match(author).group(1)
        
    
        item['pic_url'] = ''
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(self.release_time,u'%Y-%m-%d %H:%M'))
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False