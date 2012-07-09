#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from scrapy.selector import HtmlXPathSelector
from yowa.items import ContentItem

class Parser(Base):
    name = 'pconline_xw_2'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        content_node = self.hxs.select("//div[@class = 'art_con']").extract()
        content_node = PyQuery(content_node[0])
        
        content_node.remove('div[class = "pconline_page"]')
        content_node.remove('div[class = "pc3g"]')
        content_node.remove('div[class = "pageTips"]')
        content_node.remove('div[class = "art_nav_box mt10"]')
        content_node.remove('div[class = "art_bottom"]')
        content_node.remove('div[class = "art_con_top"]')

        

        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = self.hxs.select("//h1/text()").extract()[0]
        if not item['title']:
            item['title'] = self.title = self.hxs.select("//div[@id = 'UC_newsInfoDetail_lbl_newsTitle']/text()").extract()[0]
        item['content'] = self.content = content_node.__unicode__()
        release_time = self.hxs.select("//div[@class = 'art_con_top']").extract()[0]
        doc_t = PyQuery(release_time)
        release_time = doc_t('span').text()
        p = re.compile(u'20\d\d年\d\d月\d\d日')
        #item['release_time'] = self.release_time = doc('div[class="art_con_top"]').find('span').eq(0).text()
        item['release_time'] = self.release_time = p.search(release_time).group()
        item['source'] = u'pconline'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
