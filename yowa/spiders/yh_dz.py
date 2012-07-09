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
    name = 'dz_yh'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'dz', child_mark = 'yh')
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
            
    def parse_lady8844(self, response):
        '''爱美网'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'tdtitcon']/a/@href").extract()
        # the shop name
        s = re.compile(u'\[(.*?)\]')
        shop_all = hxs.select("//td[@class = pink]/text()").extract()
        meta['shop'] = []
        for shop in shop_all:
            shop_name = s.search(shop)
            if shop_name:
                meta['shop'].append(shop_name.group(1))
            else:
                meta['shop'].append(' ')
        # the valitidy time
        meta['valitidy'] = []
        # the city
        meta['city'] = hxs.select("//div[@class = 'dcweizhi']/strong/text()").extract()[0]
        c = re.compile(u'(.*?)打折')
        meta['city'] = c.search(meta['city']).group(1)

        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)
            
    def parse_sozhe(self, response):
        '''搜折网'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//a[@class = 'dzkb2']/@href").extract()
        # the shop name
        shop_all = hxs.select("//a[@class = 'dzkb2']/text()").extract()
        s = re.compile(u'(.*?)_')
        meta['shop'] = []
        for shop in shop_all:
            shop_name = s.search(shop)
            if shop_name:
                meta['shop'].append(shop_name.group(1))
            else:
                meta['shop'].append(' ')
        # the valitidy time
        valitidy_all = hxs.select("//td[@class = 'font-gray']/text()").extract()
        v = re.compile(u'-(.*?)\]')
        meta['valitidy'] = []
        for valitidy in valitidy_all:
            meta['valitidy'].append(v.search(valitidy).group(1))
        # the city
        meta['city'] = u'北京'
        
        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)       
    
    def parse_jinti(self, response):
        '''今题网'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//h3/a/@href").extract()
        # the shop name
        meta['shop'] = []
        # the valitidy time
        meta['valitidy'] = []
        # the city
        meta['city'] = hxs.select("//div[@class = 'inner_adr']/p/a[4]/text()").extract()[0]
        
        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)
            
            
    def parse_zhugou(self, response):
        '''助购'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table[@id = 'table']//tr/td[3]/a/@href").extract()
        # the shop name
        shop_all = hxs.select("//table[@id = 'table']//tr/td[4]/text()").extract()
        meta['shop'] = []
        for shop in shop_all:
            meta['shop'].append(shop)
        # the valitidy time
        valitidy_all = hxs.select("//table[@id = 'table']//tr/td[5]/text()").extract()
        v = re.compile(u'\/(\d\d-\d\d)')
        meta['valitidy'] = []
        for valitidy in valitidy_all:
            meta['valitidy'].append(v.search(valitidy).group(1))
        # the city
        meta['city'] = u'北京'
        
        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)
            
            
            
    def parse_zazheo(self, response):
        '''打折哦'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//tbody[contains(@id,'normalthread_')]//th[@class = 'new']/a/@href").extract()
        # the shop name
        s = re.compile(u'\[(.*?)\]')
        shop_all = hxs.select("//tbody[contains(@id,'normalthread_')]//th[@class = 'new']/a/text()").extract()
        meta['shop'] = []
        for shop in shop_all:
            meta['shop'].append(s.search(shop).group(1))
        # the valitidy time
        valitidy_all = hxs.select("//tbody[contains(@id,'normalthread_')]//th[@class = 'new']/a/text()").extract()
        v = re.compile(u'～(\d\d\d\d.*)')
        meta['valitidy'] = []
        for valitidy in valitidy_all:
            meta['valitidy'].append(v.search(valitidy).group(1))
        # the city
        meta['city'] = u'北京'
        
        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)
            
            
    def parse_dazhe021(self, response):
        '''上海打折网'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//tbody[contains(@id,'normalthread')]//th[@class = 'common']/a[@class = 'xst']/@href").extract()
        hxs_a.extend(hxs.select("//th[@class='new']//a[@class = 'xst']/@href").extract())
        # the shop name
        meta['shop'] = []
        # the valitidy time
        meta['valitidy'] = []
        # the city
        meta['city'] = u'上海'
        
        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)
            
            
    def parse_shanghaining(self, response):
        '''上海人'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//a[contains(@id,'imgThread_')]/@href").extract()
        # the shop name
        meta['shop'] = []
        # the valitidy time
        meta['valitidy'] = []
        # the city
        meta['city'] = u'北京'
        
        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)
            
    def parse_shenghuomei(self, response):
        '''生活美'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//tbody[contains(@id,'normalthread')]//a[@class = 'xst']/@href").extract()
        # the shop name
        meta['shop'] = []
        # the valitidy time
        meta['valitidy'] = []
        # the city
        meta['city'] = ''
        
        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)
            
    def parse_livnj(self, response):
        '''生活南京'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//a[@class = 'linkbig']/@href").extract()
        # the shop name
        s = re.compile(u'【(.*?)】')
        shop_all = hxs.select("//a[@class = 'linkbig']/font/text()").extract()
        meta['shop'] = []
        for shop in shop_all:
            shop_name = s.search(shop)
            if shop_name:
                meta['shop'].append(shop_name.group(1))
            else:
                meta['shop'].append(' ')
        # the valitidy time
        valitidy_all = hxs.select("//a[@class = 'linkbig']/font/text()").extract()
        v = re.compile(u'-(\d\d?\.\d\d?)')
        meta['valitidy'] = []
        for valitidy in valitidy_all:
            v_all = v.search(valitidy)
            if v_all:
                meta['valitidy'].append(v_all.group(1))
            else:
                meta['valitidy'].append(' ')
        # the city
        meta['city'] = u'南京'

        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)
            
            
    def parse_cocoren(self, response):
        '''爱尚网'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@id = 'List_TextA']//a/@href").extract()
        # the shop name
        meta['shop'] = []
        # the valitidy time
        meta['valitidy'] = []
        # the city
        meta['city'] = hxs.select("//div[@id = 'List_Path']/text()").extract()[2]
        c = re.compile(u'&gt;(.*?)商场打折')
        meta['city'] = c.search(meta['city'])
        if meta['city']:
            meta['city'] = meta['city'].group(1)
        
        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)
            
    def parse_zzdazhe(self, response):
        '''打折网'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//h2/a/@href").extract()
        # the shop name
        meta['shop'] = []
        # the valitidy time
        meta['valitidy'] = []
        # the city
        meta['city'] = u'郑州'
        
        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)

    def parse_360buy(self, response):
        '''京东'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class = 'list-h'][1]/li/div[@class = 'p-img']/a/@href").extract()
        # the shop name
        meta['shop'] = []
        # the valitidy time
        meta['valitidy'] = []
        # the city
        meta['city'] = u'全国'
        
        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            meta['shop'].append('京东')
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)

    def parse_shhbm(self, response):
        '''上海打折网'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'box1']/a/@href").extract()
        # the shop name
        shop_all = hxs.select("//span[@class = 'note_1']/a/text()").extract()
        meta['shop'] = []
        for shop in shop_all:
            meta['shop'].append(shop)
        # the valitidy time
        valitidy_all = hxs.select("//div[@class = 'box2']/text()").extract()
        v = re.compile(u'-(\d\d\d\d.*?日)')
        meta['valitidy'] = []
        for valitidy in valitidy_all:
            v_all = v.search(valitidy)
            if v_all:
                meta['valitidy'].append(v_all.group(1))
            else:
                meta['valitidy'].append(' ')
        # the city
        meta['city'] = u'上海'

        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1

            yield Request(url = a, meta = meta, callback = self.parse_item)
            
    def parse_12580777(self, response):
        '''12580'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class = 'dec-list']/h1/a/@href").extract()
        # the shop name
        meta['shop'] = hxs.select("//ul[@class = 'dec-list']/h1/a/text()").extract()
        # the valitidy time
        meta['valitidy'] = []
        # the city
        meta['city'] = hxs.select("//meta[@http-equiv = 'Description']/@content").extract()[0]
        c = re.compile(u'((.*?)商户折扣)')
        meta['city'] = c.search(meta['city']).group(2)
        
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
        item['sum_mark'] = 'dz'
        item['child_mark'] = 'yh'
        if len(meta['shop'])>0:
            item['merchant'] = meta['shop'][meta['num']]
        if len(meta['valitidy'])>0:
            item['deadline'] = meta['valitidy'][meta['num']]
        if meta['city']:
            item['city'] = meta['city']

        return item
