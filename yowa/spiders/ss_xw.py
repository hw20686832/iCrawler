# coding: utf-8
import re
import json
import urlparse

from scrapy.http import Request
from scrapy.exceptions import NotSupported, DropItem
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from yowa.db import session
from yowa.utils import urltools
from yowa.utils import ParserManager

class SS_XW_Spider(CrawlSpider):
    name = 'ss_xw'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'xw', child_mark = 'ss')
        for m in missions:
            try:
                meta = {'spider': self.name,
                        'domain': urltools.get_domain(m[0]),
                        'mission': m}
                if 'chinawatch-clock' in meta['domain']:
                    meta['domain'] = "chinawatch_clock"
                yield Request(url = m[0],
                              meta = meta,
                              callback = self.__getattribute__('parse_%s' % meta['domain']))
            except:
                continue

    def parse_sohu(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='center']/div[@class='list14']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='main area']/div[@class='lc']/div[@class='f14list']/ul/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sina(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='newList']/ul/li/span/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='main']/ul/li/h4/a/@href").extract())
        hxs_a.extend(hxs.select("//tbody[@id='wzcList']/tr/td[@class='sp']/a/@href").extract())
        rc = re.compile('\{"title":".*?","url":"(.*?)","subtitle":".*?","time":".*?"\},')
        hxs_a.extend(rc.findall(response.body))

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_163(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='content']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='content']/ul[@class='f12bla']/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_qq(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id='listZone']//a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='leftList']//ul/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_chinawatchnet(self, response):
        '''中国钟表网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='f14bla']//a/@href").extract()
        hxs_a.extend(hxs.select("//tr[@class='t12deegreyline']//td[@align = 'left']/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_chinawatch_clock(self, response):
        '''中国钟表'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//tr[@class='t12deegreyline']//td[@align = 'left']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_6340(self, response):
        '''搭配网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//h3/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_rayli(self, response):
        '''瑞丽服饰网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'contleftxiatitle01 txt1']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_xiumei(self, response):
        '''秀美网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//h4/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_item(self, response):
        meta = response.meta
        try:
            pm = ParserManager(meta['domain'])
        except ImportError:
            raise NotSupported('Have no supported Template for domain:%s' % meta['domain'])

        item = {}
        match = False
        for tpl in pm.list():
            p = pm.create(tpl, response = response)
            try:
                item = p.extract()
                match = p.isMatch()
                if match:
                    break
            except:
                continue

        if not match:
            raise DropItem('This page has not been extracted!')
        item['father_url_number'] = meta['mission'][1]
        item['child_url'] = response.url
        item['sum_mark'] = meta['mission'][3]
        item['child_mark'] = meta['mission'][4]

        return item
