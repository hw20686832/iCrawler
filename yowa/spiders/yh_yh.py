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
    name = 'yh_yh'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'yh', child_mark = 'yh')
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
            
    def parse_dianping(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//h2/a/@href").extract()
        # the shop name
        s = re.compile(u'\[(.*?)\]')
        shop_all = hxs.select("//h2/a/text()").extract()
        meta['shop'] = []
        for shop in shop_all:
            meta['shop'].append(s.search(shop).group(1))
        # the valitidy time
        valitidy_all = hxs.select("//div[@class = 'content']/ul/li[1]/text()").extract()
        v = re.compile(u'(\d\d\d\d-\d\d-\d\d)')
        meta['valitidy'] = []
        for valitidy in valitidy_all:
            meta['valitidy'].append(v.search(valitidy).group(1))
        # the city
        meta['city'] = hxs.select("//a[@class = 'loc-btn']/span/text()").extract()[0]
        c = re.compile(u'(.*?)站')
        meta['city'] = c.search(meta['city']).group(1)
        
        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)
            
    def parse_bj100(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//p[@class = 'bt']/a/@href").extract()
        # the shop name
        shop_all = hxs.select("//p[@class = 'bt']/a/text()").extract()
        meta['shop'] = []
        for shop in shop_all:
            meta['shop'].append(shop)
        # the valitidy time
        meta['valitidy'] = []
        # the city
        meta['city'] = hxs.select("//p[@class = 'city']/a[@class = 'now']/text()").extract()[0]
        
        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)       
    
    def parse_qq(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//a[@class = 'title cmcList']/@href").extract()
        # the shop name
        s = re.compile(u'【(.*?)】')
        shop_all = hxs.select("//a[@class = 'title cmcList']/h4/text()").extract()
        meta['shop'] = []
        for shop in shop_all:
            meta['shop'].append(s.search(shop).group(1))
        # the valitidy time
        valitidy_all = hxs.select("//p[@class = 'time']/text()").extract()
        v = re.compile(u'(\d\d\d\d.*)')
        meta['valitidy'] = []
        for valitidy in valitidy_all:
            meta['valitidy'].append(v.search(valitidy).group(1))
        # the city
        meta['city'] = []
        meta['city'] = hxs.select("//div[@class = 'current_city']/h3/text()").extract()[0]
        
        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)
            
            
    def parse_fantong(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'title']/h3/a/@href").extract()
        # the shop name
        meta['shop'] = []
        # the valitidy time
        meta['valitidy'] = []
        # the city
        meta['city'] = hxs.select("//strong[@class = 'cur-city']/text()").extract()[0]
        
        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)
            
    def parse_xixik(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class = 'CouponTextList'][1]//div[@class = 'title']/a[2]/@href").extract()
        # the shop name
        s = re.compile(u'\[(.*?)\]')
        shop_all = hxs.select("//ul[@class = 'CouponTextList'][1]//div[@class = 'title']/a[1]/text()").extract()
        meta['shop'] = []
        for shop in shop_all:
            meta['shop'].append(s.search(shop).group(1))
        # the valitidy time
        valitidy_all = hxs.select("//ul[@class = 'CouponTextList'][1]//div[@class = 'title']/text()[2]").extract()
        v = re.compile(u'(\d\d\d\d.*)')
        meta['valitidy'] = []
        for valitidy in valitidy_all:
            meta['valitidy'].append(v.search(valitidy).group(1))
        # the city
        meta['city'] = hxs.select("//div[@id = 'head_text']/strong/text()").extract()[0]
        
        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)
            
            
    def parse_yuele(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'coupon_centent']/h3/a/@href").extract()
        # the shop name
        s = re.compile(u'\[(.*?)\]')
        shop_all = hxs.select("//div[@class = 'coupon_centent']/h3/a/text()").extract()
        meta['shop'] = []
        for shop in shop_all:
            meta['shop'].append(s.search(shop).group(1))
        # the valitidy time
        valitidy_all = hxs.select("//div[@class = 'coupon_bottom']/span[1]/text()").extract()
        v = re.compile(u'(\d\d\d\d.*)')
        meta['valitidy'] = []
        for valitidy in valitidy_all:
            meta['valitidy'].append(v.search(valitidy).group(1))
        # the city
        meta['city'] = hxs.select("//span[@id = 'current_city_name']/text()").extract()[0]
        
        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)

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
        item['sum_mark'] = 'yh'
        item['child_mark'] = 'yh'
        if len(meta['shop'])>0:
            item['merchant'] = meta['shop'][meta['num']]
        if len(meta['valitidy'])>0:
            item['deadline'] = meta['valitidy'][meta['num']]
        item['city'] = meta['city']

        return item
