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

class QC_XW_Spider(CrawlSpider):
    name = 'qc_xw'
    
    def start_requests(self):
        missions = session.getMission(sum_mark = 'xw', child_mark = 'qc')
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

    def parse_sina(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='sina-16 column ']//ul/li/a/@href").extract()
        rc = re.compile('auto_news\[\d+\] = \[".*?","(.*?)",".*?",".*?"\];')
        hxs_a.extend(rc.findall(response.body))

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_163(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='content']/ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_qq(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='leftList']//ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='mod newslist']//a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_autohome(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id='ArticlesTitles']/div[@id='ArticlesTitlesLeft']//a[@id]/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sohu(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='list14']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='area carScore']/div[@class='carNews1']/div[@class='carNewsContext1']/li//a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='tabModel']/div/div/i/strong/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_bitauto(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='list_date']/ul/li/span/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_pcauto(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='wrap']//div/ul/li/strong/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_xcar(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='borderTRL_box']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='SList1']/ul[@class='threelist1_nt']/li[@span='text1']/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_chnsuv(self, response):
        '''联合越野网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='main_list']/ul/li/a/@href").extract()

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
