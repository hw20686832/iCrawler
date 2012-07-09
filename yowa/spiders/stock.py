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

class STOCK_Spider(CrawlSpider):
    name = 'stock'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'ghb',child_mark = 'gp')
        for m in missions:
            try:
                meta = {'spider': self.name,
                        'domain': urltools.get_domain(m[8]),
                        'mission': m}
                yield Request(url = 'http://hq.sinajs.cn/list=' + m[8],
                              meta = meta,
                              callback = self.parse_sinajs)
            except:
                continue

    def parse_sinajs(self, response):
        '''新浪'''
        meta = response.meta
        content_gp = response.body
        
        g = re.compile(u"\"(.*?),(.*?),(.*?),(.*?),.*,(.*?),(.*?)\"")
        meta['code'] = g.search(content_gp).group(1)
        print meta['code']
        meta['today_date'] = g.search(content_gp).group(5)
        meta['opening'] = g.search(content_gp).group(2)
        meta['closing'] = g.search(content_gp).group(4)


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
        item['source'] = u'新浪'
        item['sum_mark'] = 'ghb'
        item['child_mark'] = 'gp'
        item['child_url'] = url
        item['content'] = '<p>content</p>'
        item['father_url_number'] = meta['today_date']
        item['image_urls'] = ''
        item['type'] = 'gp'
        item['pic_url'] = ''
        #print item
        return item
    