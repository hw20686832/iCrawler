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

class LY_XW_Spider(CrawlSpider):
    name = 'ly_xw'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'xw', child_mark = 'ly')
        for m in missions:
            try:
                if urltools.get_domain(m[0]) == 'aoyou':
                    meta = {'mission': m, 'spider': self.name, 'domain': urltools.get_domain(m[0]), 'simulate': True}
                else:
                    meta = {'mission': m, 'spider': self.name, 'domain': urltools.get_domain(m[0])}
                yield Request(url = m[0],
                              meta = meta,
                              callback = self.__getattribute__('parse_%s' % meta['domain']))
            except:
                continue

    def parse_sohu(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='main area']/div[@class='lc']/div[@class='f14list']/ul/li/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_aoyou(self, response):
        meta = response.meta
        meta.__delitem__('simulate')
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id='div_newsList']/ul[@class='w_left_list']/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = meta, callback = self.parse_item)

    def parse_163(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='content']/ul[@class='list_f14d']/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_elong(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='zx-li30']/ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_iouter(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div/a[@class='nLink']/@href").extract()
        hxs_a.extend(hxs.select("//table[@id='dlNews']/tr/td/a[@class='imgLink']/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_8264(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='list']/div[@class='topic-content']//h2/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='stockul']//ul[@class='tempul']/li/a/@href").extract())
        if not hxs_a:
            hxs_a = hxs.select("//h2/a/@href").extract()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sina(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table[@class='jdkbb jdkbb12']/tr/td/a/@href").extract()

        rc = re.compile('auto_news\[\d+\] = \[".*?","(.*?)",".*?",".*?"\];')
        hxs_a.extend(rc.findall(response.body))

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_18023(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@class='inddline']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_91ski(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='newsList']/dl/dt/a/@href").extract()

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
            
    def parse_lvping(self, response):
        '''驴评网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//h3/a/@href").extract()

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
