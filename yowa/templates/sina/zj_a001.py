#coding: utf-8 
import re

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'sina001'
    

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div#artibody1')
        if not content_node:
            content_node= doc('div#artibody')
        if not content_node:
            content_node = doc('div.moduleParagraph')
        content_node.remove('script')
        content_node.remove('#contentPlayer')
        content_node.remove('span.contentPlayer')
        content_node.remove('#blkComment otherContent_01')
        content_node.remove('style')
        content_node.remove('embed')
        content_node.remove('iframe')
        content_node.remove('div[style = "text-align: right;padding-right:10px;"]')
        content_node.remove('div[style = "text-align: right;padding-right:100px;"]')
        content_node.remove('div[style = "clear:both;margin-bottom:15px;margin-top:30px;font-size:14px;"]')
        content_node.remove('div[style = "margin:20px auto 0;text-align:right; line-height:20px;"]')
        content_node.remove('div[style = "margin-top:20px;"]')
        content_node.remove('span[style = "margin-right:300px;"]')
        content_node.remove('div.corrTxt_01')
        content_node.remove('div#zfwb')
        content_node.remove('div.Ni_B1')
        content_node.remove('div.Ni_B2')
        content_node.remove('div#sinashareto')
        content_node.remove('div.otherContent_01')
        content_node.remove('div.pb')
        content_node.remove('p.page')
        content_node.remove('div.xg')
        content_node.remove('div.corrTxt_01')
        content_node.remove('div.tag')
        content_node.remove('div.blkS1')
        content_node.remove('div[class = "blk-video"]')
        content_node.remove('a[href = "http://ent.sina.com.cn/f/v/waptuiguang.html"]')
        content_node.remove('a[href = "http://sports.sina.com.cn/nba_in_wap.html"]')
        content_node.remove('div.news_block')


        item = ContentItem()
        
        item['title'] = self.title = doc('h1[id = "artibodyTitle"]').text()
        if item['title'] == None:
            item['title'] = self.title = doc('h1[id = "article-title"]').text()
        if item['title'] == None:
            item['title'] = self.title = doc('h2[id = "artibodyTitle"]').text()
        
        item['release_time'] = self.release_time = doc('span#pub_date').text()
        if self.release_time ==None:
            self.release_time = doc('p[class = "source"]').text()
        if self.release_time ==None:
            self.release_time = doc('p[class = "from_info"]').text()
        if self.release_time ==None:
            self.release_time = doc('h2').eq(0).text()
        p = re.compile(u"(20\d\d.*\d\d:\d\d)")
        item['release_time'] = self.release_time = p.search(self.release_time).group()
            
        
        item['source'] = u"新浪"
        item['author'] = ''
        item['pic_url'] = ''

        imgs = content_node('img')
        image_urls = []
        for img in imgs:
            if ".gif" in img.get('src').lower():
                continue
            if not img.get('src'):
                continue
            else:
                imgs.eq(imgs.index(img)).before('<br>')
                imgs.eq(imgs.index(img)).append('<br>')
                image_urls.append(self.getRealURI(img.get('src')))
        item['image_urls'] = image_urls
        
        del_table = content_node('table')
        for d in del_table:
            if d.get('align'):
                del_table.eq(del_table.index(d)).attr['align'] = ''
        content = content_node.__unicode__()
        item['content'] = self.content = content
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
