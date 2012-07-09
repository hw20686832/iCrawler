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

class SZ_XW_Spider(CrawlSpider):
    name = 'sz_xw'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'xw', child_mark = 'sz')
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
        hxs_a.extend(hxs.select("//div[@id='articleList']/ul/li/a/@href").extract())
        

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sina(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='list_009']/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='fixList']/ul/li/a/@href").extract())
        if not hxs_a:
            scrpit = hxs.select("//div[@class = 'main']//script/text()").extract()
            hxs_a = re.findall('auto_news\[\d*\].*?","(.*?)","',scrpit[0])

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sohu(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@class='newsblue1']/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='f14list']/ul/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_163(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='bd clearfix']/div/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='content']/ul[@class='list_f14d']/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='bd clearfix']//ul[@class='list-1 mb15']/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='content']/ul/li/a/@href").extract())
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_xilu(self, response):
        '''西陆网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='listbox']/dl//a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_huanqiu(self, response):
        '''环球网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='section']//ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_people(self, response):
        '''人民网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='dot_14']//li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='one_5 d2_15 d2tu_3 d2tu_4']/ul/li//a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_qianlong(self, response):
        '''千龙网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id = 'more']//a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_chinanews(self, response):
        '''中国新闻网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'dd_bt']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_gongyishibao(self, response):
        '''公益时报'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'class_list']/ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_ifeng(self, response):
        '''凤凰网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'newsList']/ul/li/a/@href").extract()

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
