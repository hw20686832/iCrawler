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

class SM_XW_Spider(CrawlSpider):
    name = 'sm_xw'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'xw', child_mark = 'sm')
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
        hxs_a = hxs.select("//div[@class='list02']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='area']//div[@id='newsList']/div/div[@class='scroll_block']/div[@class='scroll_news']/a/@href").extract())
        if not hxs_a:
            hxs_a = hxs.select("//div[@class = 'scroll_news']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sina(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='conList']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='contList']/ul/li/a/@href").extract())
        hxs_a.extend(hxs.select("//ul[@class='dot14']/li//a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='NewListCtr02List linklistStyle']//li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_163(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='col1LBg']/div[@class='leftList']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='content']/ul/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='bd clearfix']/div/ul/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_qq(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='main']/div[@class='mod newslist']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='leftList']//ul/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_cnmo(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='div_body']/div[@class='bodyW']//div[@class='aLN1' or @class='aLN2']/div[@class='nlPic']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_zol(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='news_box']/div[@class='news_list']/div[@class='news_tit']//a[2]/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='Em']/div[@class='manu_em_2']/ul[@class='mt10']/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='Em_2']/ul/li/a/@href").extract())
        if not hxs_a:
            hxs_a = hxs.select("//h4/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_pconline(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='main']//ul[@class='ulList img1']/li/div[@class='title']/b/a[2]/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='bbsArtList']/ul/li/p[@class='title']/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='tb']/ul/li/div[@class='title']/b/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='pcbox_6']/ul[@class='ln24 f14px']/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_pcpop(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='contain1']/div[@class='left_contain1']/ul[@class='list']/li/div/span/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='pb4']/div[@class='pb41']/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_it168(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='w980']/div[@class='l4_2']/ul/li/em/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_178(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id='content-left']/div[@class='article']//h2/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_tgbus(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='hide']/div[@class='list']//b/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_yesky(self, response):
        '''天极网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='list']//li//strong/a/@href").extract()
        if not hxs_a:
            hxs_a = hxs.select("//ul[@class = 'listbox1']/li/strong/a/@href").extract()

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
