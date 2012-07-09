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

class NewsSpider(CrawlSpider):
    name = 'kj_xw'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'xw', child_mark = 'kj')
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
        hxs_a = hxs.select("//div[@class='conList']//a/@href").extract()
        hxs_a.extend(hxs.select("//ul[@class='list_009']//a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='contList']//a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='show_data']//ul/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_yahoo(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='list']//a/@href").extract()
        hxs_a.extend(hxs.select("//ul[@class='list_body']/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sohu(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='list02']//a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='txt01']//h1/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='newsList']/div/div[@class='scroll_block']/div[@class='scroll_news']/a/@href").extract())
        hxs_a.extend(hxs.select("//td[@class='fclist']//a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_qq(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='leftList']//ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='mod newslist']/ul/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_people(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='list']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//td[@class='t14l14']/a/@href").extract())
        hxs_a.extend(hxs.select("//table[@class='list03_2j']/tr/td/a/@href").extract())
        hxs_a.extend(hxs.select("//td[@class='news01']/a/@href").extract())
        hxs_a.extend(hxs.select("//td[@class='t10l14bl']/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_163(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='content']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='tList14px']/ul/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_huanqiu(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='content']/div[@class='main']/ul/li/span/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='textlist']/ul/li/a/@href").extract())
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_astron(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table[@class='listarticle']/tr/td//a/@href").extract()
        if not hxs_a:
            hxs_a = hxs.select("//a[@class = 'pic']/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_alibuybuy(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='content']/div[@class='breadcrumb']/ul[@class='explist viewlist']/li//h3/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_bioon(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id='region-column1-layout2']/div[@class='padding-top-5 padding-bottom-9']/h2/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='list']/ul/li/a/@href").extract())
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_cas(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//a[@class='outh14z']/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_cdstm(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='sn_listp_l']/ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_cenews(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id='text_list']/ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_chinanews(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='content_list']/ul/li/div[@class='dd_bt']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_dkj1997(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@class='xian03']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_enet(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='list']/ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_kaogu(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@height='24']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_kxsj(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//tbody/tr[@height='25']/td/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_skylook(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//tr/td[@valign='top' and @align='left']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_ttufo(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='content_r_content_r']/div/p/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_eedu(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//h1[@class='list_news_tit']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_cusdn(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@style='padding-top:10px']/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_it_times(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='title_list']/ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_itxinwen(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='sysnews']/h5[@class='left']/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
                
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_ifeng(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='newsList']/ul/li/a/@href").extract()
        
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
