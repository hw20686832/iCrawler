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

class TY_XW_Spider(CrawlSpider):
    name = 'ty_xw'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'xw', child_mark = 'ty')
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

    def parse_qq(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='main']/div[@class='mod newslist']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='leftList']//ul/li/a/@href").extract())
        hxs_a.extend(hxs.select("//table[@class='mart10 marb10']/tr/td/a[@class='hotnews']/@href").extract())
        hxs_a.extend(hxs.select("//td[@class = 'hui']/a/@href").extract())
        hxs_a.extend(hxs.select("//td[@class='font14px font5757']/a/@href").extract())
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sohu(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='main area']/div[@class='lc']/div[@class='f14list']/ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_163(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='col2']/ul[@class='articleList']/li/span/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sina(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id='pL_Main']/div[@id='d_list']/ul/li/span/a/@href").extract()
        hxs_a.extend(hxs.select("//td[@class='l19']/a[@class='a06']/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='S_Cont_11']/a/@href").extract())
        hxs_a.extend(hxs.select("//td[@class='font14px font5757']/a/@href").extract())
        hxs_a.extend(hxs.select("//li/a/@href").extract())
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_18023(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table/tr/td[@class='inddline']/a/@href").extract()
        hxs_a.extend(hxs.select("//ul[@class='list_li']//a/@href").extract())
        if not hxs_a:
            hxs_a = hxs.select("//ul[@class = 'a7List two_col cl']/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_8264(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='l1box']/div[@class='topic-content']//div[@class='post-title']/h2/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_iouter(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table[@id='dlNews']/tr/td/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='summary']//div[@class='title']/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_91ski(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='newslist']/dl/dt/a[not(@class)]/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sport(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table/tbody/tr/td/a[@class='p1']/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_nba(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'list5-ilt']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_21cn(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id='main']/div[@class='cnt']/ul/li/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_titan24(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='txtlist']/ul/li/ul/li/a/@href").extract()
        
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

    def parse_7m(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='news']/div[@class='n_t']/div[@class='n_tz']/ul/li/a[1]/@href").extract()
        
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

    def parse_xinhuanet(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table[@class='hei14']/div[@id]/tr/td[2]/a/@href").extract()
        
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
