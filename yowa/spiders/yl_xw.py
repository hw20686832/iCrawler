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

class YL_XW_Spider(CrawlSpider):
    name = 'yl_xw'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'xw', child_mark = 'yl')
        for m in missions:
            try:
                meta = {'spider': self.name,
                        'domain': urltools.get_domain(m[0]),
                        'mission': m}
                yield Request(url = m[0],
                              meta = meta,
                              callback = self.__getattribute__('parse_%s' % meta['domain']))
            except:
                continue

    def parse_sohu(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='f14list']/ul/li/a[@rel='external']/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='main area']/div[@class='lc']/div[@class='f14list']/ul/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_qq(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='p15 lh26 f14']/table/tr/td[@class='lh26 f14']/a[@class='f50']/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='leftList']//ul/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='mod newslist']/ul/li/a/@href").extract())
        hxs_a.extend(hxs.select("//td[@class='lh26 f14']/table/tr/td/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='listZone']/span/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@style='float:left; width:495px']/a/@href").extract())
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_163(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='col1']/div[@class='leftList']/ul[@class='clearfix']/li/h5/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sina(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='contList']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//table/tr/td[@class='f14' or @class='f149']/li/a/@href").extract())
        hxs_a.extend(hxs.select("//ul[@class='list_009']/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='f14list']//li/a/@href").extract())
        hxs_a.extend(hxs.select("//td[@class='f14']/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_yahoo(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='funleft']/ul[@class='dashed']/li//p[@class='title']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_ifeng(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='main']/div[@class='left']/div[@class='newsList']/ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_xinhuanet(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table/tr/td[@class='hei14']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_btv(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table/tr/td/a[@class='tt22']/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_china(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='list']/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_21cn(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='bd']/ul[@class='txtlist']/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_cri(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='c2left620']/div[@id='more']/table/tr/td/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_chinayes(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='newslist']/li/h2[@class='hdline']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_news365(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table[@align='center']/tr/td[2]/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_hunantv(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='list']/ul/li/span[@class='title']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
                
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_people(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='list_14 clearfix']/li/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
                
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_m1905(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='newsmain']//dl[@class='classf_box']/dd[1]//a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
                
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_yule(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table[@id='table3']/tr/td/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
                
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_chinanews(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='cont']//td[@class='color065590']/a/@href").extract()
        
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
