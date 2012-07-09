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

class BlogSpider(CrawlSpider):
    name = 'all_bk'
    
    def start_requests(self):
        missions = session.getMission(sum_mark = 'bk')
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
        hxs_a = hxs.select("//div[@class='listBlk']/ul[@class='list_009']/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@id='S_Cont_11']/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class = 'blog_title']/a/@href").extract())
        hxs_a.extend(hxs.select("//span[@class = 'atc_title']/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_163(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='col1']/div[@class='leftList']/ul[@class='clearfix']/li/h5/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sohu(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='mainBox']/div/div/ul/li/span[@class='title']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_qq(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//div[@id="ifeedsMode"]/ul/li//div[@class="f_item"]').extract()
        hxs_a.extend(hxs.select("//table[@id='link1']/tr/td/a/@href").extract())
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_hexun(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id='dinglist']/dl[contains(@id, 'Recommend_')]//h2/a/@href").extract()
        if not hxs_a:
            hxs_a = hxs.select("//span[@class = 'ArticleTitleText']/a/@href").extract()
            
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_eastmoney(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//div[@class="htBox dianji"]/ul[@class="n" or @class="n s"]/li[@class="w40"]/a/@href').extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_ifeng(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='main']/div[@class='left']/div[@class='newslist']/h3/a/@href").extract()

        meta['simulate'] = True
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = meta, callback = self.parse_item)
            
    def parse_huanqiu(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//dl[@class='bbda']//dt[@class='xs2']/a[@target = '_blank']/@href").extract()

        meta['simulate'] = True
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

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
        item['sum_mark'] = meta['mission'][3]
        item['child_mark'] = meta['mission'][4]

        return item
