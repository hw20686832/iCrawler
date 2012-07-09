# coding: utf-8
import re
import json
import urlparse

from scrapy.http import Request
from scrapy.exceptions import NotSupported, DropItem
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from pyquery import PyQuery

from yowa.db import session
from yowa.utils import urltools
from yowa.utils import ParserManager

class sh_tz_Spider(CrawlSpider):
    name = 'sh_tz'
    
    def start_requests(self):
        missions = session.getMission(sum_mark = 'tz', child_mark = 'sh')
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


    def parse_cnfish(self, response):
        '''观赏鱼之家'''

        doc = PyQuery(response.body)
        text = doc('script').text()

        c = re.compile('weidunkey=(.*?)";window')
        u = re.compile('window.location = "(.*?)";')

        cook = c.search(text).group(1)
        url = u.search(text).group(1)

        cookies = {'weidunkey': cook}
        url = "http://bbs.cnfish.com"+url
        return Request(url = url, meta = response.meta, cookies = cookies,callback = self.cnfish_middle_parse)

    def cnfish_middle_parse(self,response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//tbody[contains(@id, "normalthread_")]//td[@class="icn"]/a/@href').extract()
        print hxs_a
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_yoka(self,response):
        ''' YOKA时尚网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'b1cen3 jd']/dl//u[@class = 'a0']/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_525j(self,response):
        '''我爱我家知道网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table[@width = '100%']/tbody/tr/th/a[@class = 'title']/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_tumanduo(self,response):
        '''装修图满多'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'block2']/div[@class = 'Notop']/table//tr/td/a[contains(@href,'gp')]/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_zhaogewo(self,response):
        '''找个窝'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'dw1 daiq_listbg']/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_39(self,response):
        '''39健康问答'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//li[contains(@onmouseover,'this.className')]/span[@class = 'tit']/a[contains(@href,'question')]/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_120ask(self,response):
        '''有问必答网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@class = 'questitle']/a[@class = 'listHref2']/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_mypethome(self,response):
        '''宠物之家'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@id = 'postmessage_344589']//a[contains(@href,'mypethome')]/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_movshow(self, response):
        '''猫咪有约'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//tbody[contains(@id,'normalthread')]//th[@class = 'new']/a[@class = 'xst']/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_goumin(self, response):
        '''狗民网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//span[@class = 'f14']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_xcar(self, response):
        '''爱卡汽车网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='pictxt_nt4']/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_autohome(self, response):
        '''汽车之家'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table[@class='topicList ma_t2']//a[@class='font14']/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_dazhe021(self, response):
        '''上海打折网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//tbody[contains(@id,'normalthread')]//th[@class = 'common']/a[@class = 'xst']/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_99wed(self, response):
        '''久久结婚'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@class = 'th y-style']/h3/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_chepeng(self, response):
        '''车朋网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class = 'articleList']//a/@href").extract()

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

