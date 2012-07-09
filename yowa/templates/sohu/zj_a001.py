#coding: utf-8
import re

from pyquery import PyQuery

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'sohu001'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div#contentText')
        if not content_node:
            content_node = doc('div[id *= "news_c"]')
        if not content_node:
            content_node = doc('div.textcont')
        if not content_node:
            content_node = doc('div.txt')
        
        content_node.remove('script')
        content_node.remove('style')
        content_node.remove('.line')
        content_node.remove('#shareIn')
        content_node.remove('.tagHotg')
        content_node.remove('.blank8')
        content_node.remove('."editShare clear"')
        content_node.remove('select')
        #content_node.remove('table[width = "100%"]')('td[align = "center"]')
        content_node.remove('div[class = "jingbian_travel01_04"]')
        content_node.remove('div[class = "txt2"]')
        content_node.remove('iframe')
        content_node.remove('embed')
        content_node.remove('td[style = "font-size: 14px; font-weight: bold;"]')
        content_node.remove('table[style = "margin-right: 20px;"]')
        content_node.remove('digi_perpage_bottom')
        content_node.remove('div[class = "extract clear"]')
        content_node.remove('table[bgcolor = "#eeeeee"]')
        #content_node.remove('img[alt = "搜狐教育频道"]')
        content_node.remove('table[bgcolor = "#e2e2e2"]')
        content_node.remove('table[bgcolor = "#66ccff"]')
        content_node.remove('div[class = "digi_digest"]')
        content_node.remove('div.l')
        content_node.remove('div.z2')
        content_node.remove('form')
        content_node.remove('img[width = "511"][height = "33"]')
        content_node.remove('img[width = "471"][height = "75"]')
        content_node.remove('div.talk')
        content_node.remove('img[width="598"][height="53"]')
        content_node.remove('div[id = "cms4_zutu_nav1"]')
        content_node.remove('table[bgcolor="#f5f5f5"]')
        content_node.remove('img[width="200"][height="60"]')


        item['title'] = self.title = doc('h1').text()
        if item['title'] == None:
            item['title'] = self.title = doc('div.title').text()
        
        if self.title == u'我来说两句':
            item['title'] = self.title = doc('title').text()
        
        
        
        item['release_time'] = self.release_time = doc('div.sourceTime')('div.r').text()
        if item['release_time'] == None:
            item['release_time'] = self.release_time = doc('div.time').text()
        if item['release_time'] == None:
            item['release_time'] = self.release_time = doc('div[class = "news_41 left"]').text()
        if item['release_time'] == None:
            item['release_time'] = self.release_time = doc('div.rq').text()
        if item['release_time'] == None:
            item['release_time'] = self.release_time = doc('div[class = "function clear"]')('div.l').text()
        if item['release_time'] == None:
            item['release_time'] = self.release_time = doc('div.date')('span').text()
        if item['release_time'] == None:
            item['release_time'] = self.release_time = doc('span.time').text()
        if item['release_time'] == None:
            item['release_time'] = self.release_time = doc('div[id = "club_artinputdate"]').text()
        if item['release_time'] == None:
            self.release_time = doc('div.source').text()
            t = re.compile(u'20\d\d.*-\d\d')
            if self.release_time:
                self.release_time = t.search(self.release_time)
                if not self.release_time:
                    self.release_time = doc('h3').text()
                    t = re.compile(u'20\d\d.*:\d\d')
                    self.release_time = t.search(self.release_time)
                if self.release_time:
                    item['release_time'] = self.release_time = self.release_time.group()
        
        item['source'] = self.source = u"搜狐"
        item['author'] = doc('.l')('a').eq(0).text()
        item['pic_url'] = ''
        
        imgs = content_node('img')
        image_urls = []
        for img in imgs:
            if not img.get('src'):
                continue
            elif ".gif" in img.get('src'):
                continue
            else:
                imgs.eq(imgs.index(img)).append('<br><p>')
                imgs.eq(imgs.index(img)).before('<br>')
                image_urls.append(self.getRealURI(img.get('src')))
        item['image_urls'] = image_urls
        
        content = content_node.__unicode__()
        content = content.replace('&#13;','')
        content = content.replace(u'[点击图片进入下一页]','')
        
        if not item['image_urls']:
            if doc('img#slide_pic').attr('src'):
                item['image_urls'] = [doc('img#slide_pic').attr('src'),]
                content = '<img src="'+item['image_urls'][0]+'"><br><br>'+content
        
        
        
        item['content'] = self.content = content

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
