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

class CQ_CQ_Spider(CrawlSpider):
    name = 'cq_cq'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'cq', child_mark = 'cq')
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
            
    def parse_cbex(self, response):
        '''  北京产权交易所'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//tr[@class='height23']//a/@href").extract()
        if not hxs_a:
            hxs_a = hxs.select("//td[@class = 'qytprotd2 proleft']/a/@href").extract()
        if not hxs_a:
            hxs_a = hxs.select("//a[@class = 'artitlelist']/@href").extract()
        if not hxs_a:
            hxs_a = hxs.select("//td[@class = 'qytinvtd2 proleft']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_tprtc(self, response):
        '''  天津产权交易中心'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//tr[contains(@onclick,'/transaction/project/jiaoyixinxi')]/@onclick").extract()

        for a in hxs_a:
            a = a.replace("javascript:window.open('","")
            a = a.replace("')","")
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_suaee(self, response):
        '''  上海联合产权交易所'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//a[@class='proj']/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_cquae(self, response):
        '''  重庆联合产权交易所'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@style='word-break:break-all;']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_cfae(self, response):
        '''  北京产权交易所'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//tr[@class='height23']//a/@href").extract()
        if not hxs_a:
            hxs_a = hxs.select("//td[@class = 'qytprotd2 proleft']/a/@href").extract()
        if not hxs_a:
            hxs_a = hxs.select("//a[@class = 'artitlelist']/@href").extract()
        if not hxs_a:
            hxs_a = hxs.select("//td[@class = 'qytinvtd2 proleft']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    
    def parse_item(self, response):
        meta = response.meta
        url = response.url
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
            
        if '/researchcontroller/' in url:
            item['release_time'] = meta['release_time'][meta['num']]
        return item
