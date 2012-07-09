# coding: utf-8
import re
import json
import urlparse
import string
import time

from scrapy.http import Request
from scrapy.exceptions import NotSupported, DropItem
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from yowa.db import session
from yowa.utils import urltools
from yowa.utils import ParserManager

class TuangouSpider(CrawlSpider):
    name = 'all_tg'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'tg')
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

    def parse_meituan(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        city = hxs.select("//div[@class='city']/h2/@sname").extract()[0]
        hxs_a = hxs.select('//div[@id="content"]/div[contains(@class, "item")]/h1/a/@href').extract()
        meta['hxs_a'] = []
        meta['num'] = 0
        meta['area'] = city.strip()
        for a in hxs_a:
            yield Request(url = a, meta = meta, callback = self.parse_item)

    def parse_lashou(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        city = hxs.select("//div[@class='header']/ul[@class='city l']/li[@class='more']//b/text()").extract()[0]
        hxs_a = hxs.select('//div[@class="con-list"]/ul/li/div[@class="con-pic"]/a/@href').extract()
        meta['hxs_a'] = []
        meta['num'] = 0

        meta['area'] = city.strip()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = meta, callback = self.parse_item)

    def parse_nuomi(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        city = hxs.select("//div[@class='change_city']/strong/text()").extract()[0]
        meta['deadline'] = hxs.select('//ul[@id="sortList"]//div[@class = "surplus-num"]/@endtime').extract()
        hxs_a = hxs.select('//ul[@id="sortList"]/li/h3/a/@href').extract()
        meta['hxs_a'] = hxs_a
        meta['num'] = 0
        
        num = 0
        meta['area'] = city.strip()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1
            yield Request(url = re.sub('\?p=.*$', '', a), headers = response.headers, meta = meta, callback = self.parse_item)

    def parse_tuan800(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        city = hxs.select("//div[@class='city l']/span/a/text()").extract()[0]
        hxs_a = hxs.select('//div[@class="area"]/div[@class="deallist"]//div[@class="deal"]/h3/a/@href').extract()
        meta['hxs_a'] = []
        meta['num'] = 0

        meta['area'] = city.strip()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = meta, callback = self.parse_item)

    def parse_ctrip(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='group_indexlist']/li/div[@class='title']/a[1]/@href").extract()
        hxs_a.extend(hxs.select("//div[@id='productHolder']/div[@class='pkg_list layoutfix']/div[@class='details']/h3/a/@href").extract())
        meta['hxs_a'] = []
        meta['num'] = 0
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = meta, callback = self.parse_item)

    def parse_elong(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='slider']/ul/li/div[@class='productxtbar']//div[@class='deal']/span/a/@href").extract()
        meta['hxs_a'] = []
        meta['num'] = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = meta, callback = self.parse_item)

    def parse_gaopeng(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id='contentB']//ul[@class='sortList ClearFix']/li/h3/a/@href").extract()
        meta['hxs_a'] = []
        meta['num'] = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = meta, callback = self.parse_item)

    def parse_qunar(self, response):
        meta = response.meta
        meta['hxs_a'] = []
        meta['num'] = 0
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//article[@class='product_list']/ul/li/dl/dd[@class='img_show']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = meta, callback = self.parse_item)

    def parse_aoyou(self, response):
        meta = response.meta
        meta['hxs_a'] = []
        meta['num'] = 0
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='Panicbuy_tg']/div[@class='Panicbuy_tg_block']/div[@class='Panicbuy_tg_block_img']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = meta, callback = self.parse_item)
            
    def parse_gome(self, response):
        meta = response.meta
        meta['hxs_a'] = []
        meta['num'] = 0
        hxs = HtmlXPathSelector(response)
        city = hxs.select("//div[@class='member']/a[@class = 'cur']/text()").extract()[0]
        hxs_a = hxs.select('//div[@class="title"]/a/@href').extract()

        meta['area'] = city.strip()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = meta, callback = self.parse_item)
            
    def parse_360buy(self, response):
        meta = response.meta
        meta['hxs_a'] = []
        meta['num'] = 0
        hxs = HtmlXPathSelector(response)
        city = hxs.select("//div[@class='city']/h2/text()").extract()[0]
        hxs_a = hxs.select('//div[@class="title"]/a/@href').extract()

        meta['area'] = city.strip()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = meta, callback = self.parse_item)
        
    def parse_55bbs(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        city = hxs.select(u"//a[@title='全部团购']/text()").extract()[0]
        c = re.compile(u'(.*?)全部团购')
        city = c.search(city).group(1)
        meta['hxs_a'] = hxs.select('//a[@class="title"]/@href').extract()
        
        meta['content_image'] = hxs.select('//a[@class = "image_link"]/img/@src').extract()
        meta['content'] = hxs.select("//a[@class = 'title']/text()").extract()
        meta['title'] = meta['content']
        price = hxs.select("//div[@class = 'list_jg']/b/text()").extract()
        p = re.compile(u'(.*?)元')
        meta['price'] = []
        for jg in price:
            meta['price'].append(p.search(jg).group(1))
        
        meta['source'] = u'我爱团购'
        meta['area'] = city.strip()
        
        num = 0
        for a in meta['hxs_a']:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1
            
            yield Request(url = a, meta = meta, callback = self.parse_item)
            
    def parse_27(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        city = hxs.select("//div[@class='city']/h2/text()").extract()[0]
        meta['hxs_a'] = hxs.select('//div[@class="cover"]/a[1]/@href').extract()
        
        meta['price'] = hxs.select("//div[@class = 'deal-price']/b/text()").extract()
        meta['area'] = city.strip()
        
        num = 0
        for a in meta['hxs_a']:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
                
            meta['num'] = num
            num = num +1
            
            yield Request(url = a, meta = meta, callback = self.parse_item)
            
    def parse_jinantuan(self, response):
        meta = response.meta
        meta['hxs_a'] = []
        meta['num'] = 0
        hxs = HtmlXPathSelector(response)
        city = u'济南'
        hxs_a = hxs.select('//div[contains(@class,"item ")]/h1/a/@href').extract()

        meta['area'] = city.strip()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = meta, callback = self.parse_item)
            
    def parse_12580777(self, response):
        meta = response.meta
        meta['hxs_a'] = []
        meta['num'] = 0
        hxs = HtmlXPathSelector(response)
        city = hxs.select("//span[@class='f01']/text()").extract()[0]
        hxs_a = hxs.select('//h1/a/@href').extract()

        meta['area'] = city.strip()
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

        item['city'] = meta.get('area')
        item['father_url_number'] = meta['mission'][1]
        item['child_url'] = response.url
        item['sum_mark'] = meta['mission'][3]
        item['child_mark'] = meta['mission'][4]
        if len(meta['hxs_a'])>0:
            if 'out.tuan800' in meta['hxs_a'][meta['num']]:
                content_image = meta['content_image'][meta['num']]
                item['image_urls'] = [content_image,]
                image="<br/><br/><img src='"+content_image+"'>"
                content = meta['content'][meta['num']]
                content = content+image
                item['title'] = meta['title'][meta['num']]
                item['content'] =  content
                item['price'] = meta['price'][meta['num']].strip()
                item['source'] = meta['source']
            
            if 'tuan.27.cn' in response.url:
                item['price'] = meta['price'][meta['num']].strip()
                
            if 'nuomi.com' in meta['hxs_a'][meta['num']]:
                deadline = meta['deadline'][meta['num']]
                deadline = deadline[0:10]
                deadline = string.atoi(deadline)
                deadline = time.localtime(deadline)
                item['deadline'] = time.strftime('%Y-%m-%d',deadline)

        return item
