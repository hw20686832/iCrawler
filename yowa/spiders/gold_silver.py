# coding: utf-8
import re
import json
import urlparse

from scrapy.http import Request
from scrapy.exceptions import NotSupported, DropItem
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import XmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from yowa.utils import ParserManager
from yowa.db import session
from yowa.utils import urltools
from yowa.items import ContentItem

class HJ_BY_Spider(CrawlSpider):
    name = 'hj_by'

    def start_requests(self):
        missions = ['http://m.kitco.cn/gold.html','http://m.kitco.cn/silver.html']
        for m in missions:
            try:
                meta = {'spider': self.name,
                        'domain': urltools.get_domain(m),
                        'mission': m}
                yield Request(url = m,
                              meta = meta,
                              callback = self.parse_kitco)
            except:
                continue

    def parse_kitco(self, response):
        '''kitco'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        if 'gold' in response.url:
            meta['code'] = 'hj'
        if 'silver' in response.url:
            meta['code'] = 'by'
        print meta['code']
        today_date = hxs.select("//table[@width='170'][2]//tr[1]/td/font/text()").extract()[0]
        h = re.compile(u"\d\d\d\d-\d\d-\d\d")
        meta['today_date'] = h.search(today_date).group()
        meta['opening'] = hxs.select("//table[@width='170'][2]//tr[3]/td[1]/font/text()").extract()[0]
        meta['closing'] = hxs.select("//table[@width='170'][2]//tr[3]/td[2]/font/text()").extract()[0]


        yield Request(url = response.url, meta = meta, callback = self.parse_item)
          
    
    def parse_item(self, response):
        meta = response.meta
        url = response.url
        
        item = ContentItem()
        
        item['code'] = meta['code']
        print item['code']
        item['today_date'] = meta['today_date']
        item['opening'] = meta['opening']
        item['closing'] = meta['closing']
        item['source'] = u'kitco'
        item['sum_mark'] = 'ghb'
        item['child_mark'] = 'hj'
        item['child_url'] = url
        item['content'] = '<p>content</p>'
        item['father_url_number'] = meta['today_date']
        item['image_urls'] = ''
        item['type'] = 'hj'
        item['pic_url'] = ''
        #print item
        return item
    