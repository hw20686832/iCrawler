#coding: utf-8
import re
import time

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'qq001'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        doc.remove('div#tipswindow')
        content_node = doc('div#Cnt-Main-Article-QQ')
        if not content_node:
            content_node = doc('div#ArticleCnt')
        if not content_node:
            content_node = doc('div#textContent')
        if not content_node:
            content_node = doc('#content')
        if not content_node:
            content_node = doc('div[id = "qnews-content"]')
            
        content_node.remove('script')
        content_node.remove('style')
        content_node.remove('iframe')
        content_node.remove('div.adpip_Aritcle_QQ')
        content_node.remove('table#picInPic')
        content_node.remove('div.dayuw_ad')
        content_node.remove('div.tJieHot_')
        content_node.remove('div.b_new_mod')
        content_node.remove('div#awh_sports')
        content_node.remove('div[id = "photo-warp"]')
        content_node.remove('div#MorePic')
        content_node.remove('div#cmenu')
        content_node.remove('div#flashCff')
        content_node.remove('div#contTxt')
        content_node.remove('div#PGViframe')
        content_node.remove('div#Reading')
        content_node.remove('span[style = "BACKGROUND-COLOR: navy; COLOR: white"]')
        content_node.remove('img[width="592"][height="100"]')

        content = content_node.__unicode__()

        item = ContentItem()
        
        item['title'] = self.title = doc('h1').text()
        if not item['title']:
            item['title'] = self.title = doc('div#ArticleTit').text()
        if not item['title']:
            item['title'] = self.title = doc('h2').text()
            
        item['content'] = self.content = content
        
        item['release_time'] = self.release_time = doc('span.pubTime').text()
        p = re.compile(u"(20\d\d.*\d\d:\d\d)")

        if not self.release_time:
            self.release_time = doc('div[class = "info"]').text()
            if self.release_time == None:
                self.release_time = doc('div[id = "ArtFrom"]').text()
            if self.release_time == None:
                self.release_time = doc('div[class = "pubtime"]').text()
            if self.release_time == None:
                self.release_time = doc('span[id= "Freleasetime"]').text()
            if self.release_time == None:
                self.release_time = doc('td.xborderb1').eq(1).text()
                p = re.compile(u"(20.*-\d\d)")

                
            item['release_time'] = self.release_time = p.search(self.release_time).group()
        #item['release_switch_time'] = time.mktime(time.strptime(self.release_time,time_s))
            
        item['source'] = u"腾讯"
        item['author'] = ''
        item['pic_url'] = ''

        imgs = content_node('img')
        image_urls = []
        for img in imgs:
            if ".gif" in img.get('src'):
                continue
            if not img.get('src'):
                continue
            else:
                imgs.eq(imgs.index(img)).before('<br>')
                image_urls.append(self.getRealURI(img.get('src')))
        item['image_urls'] = image_urls

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
