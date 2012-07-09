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

class YX_XW_Spider(CrawlSpider):
    name = 'yx_xw'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'xw', child_mark = 'yx')
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

    def parse_sohu(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='main area']/div[@class='lc']/div[@class='f14list']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@id='content3']/div[@id='list_leftcontent']//div[@class='lan1_title']/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_qq(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='leftList' or @class='ListList']//ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//ul[@class='mod_news_list']/li/a[2]/@href").extract())
        hxs_a.extend(hxs.select("//table/tbody/tr/td/table/tr/td/a[2]/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='listZone']/ul/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='flr677']//div[@id='tplb2']/table/tr/td/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='main']/div[@class='mod newslist']/ul/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='tplb2']/table[@class='yh2']/tr/td/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sina(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@class='linkBlue']/a/@href").extract()
        hxs_a.extend(hxs.select("//ul[@class='list_009']/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='c-rcb3']/div/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='ListRight']//div[@class='ListList']/ul/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='Part']/ul/li/a[@class='biao_2']/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='d_list_txt']/ul//a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='ListList']//a/@href").extract())
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_duowan(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id='list-page']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='mod-tabs-content']/ul[@class='mod-pic-txt']/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='content']/div[@id='main']/div[@class='bg-box-t']//h2/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='list_main']//ul[@class='list']/li/span/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='cont_txt']/ul/li/span/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='main']/div[@id='list-page']/ul/li/span/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='article']/div[@id='pageMain']/ul/li/span/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='main-left']/div[@class='left']/div[@class='main-list']//h5/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='page_list']/div[@id='page_text_list']//ul/li/p/a[2]/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='new_list_right']/ul[@class='listFont']/li/span/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='center']//div[@class='newsbox']/div[@class='newstitle']/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='mod-list']//div[@class='gmaes']/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='ym-art-list']/ul[@class='list']/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='news2']/ul[@class='list']/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='list-page']/ul[@class='listFont']/li/span/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='mod-list']/div[@class='list-page']/ul[@class='art']/li/a/@href").extract())
        hxs_a.extend(hxs.select("//a[@class = 'focus_a2']/@href").extract())
        if not hxs_a:
            hxs_a = hxs.select("//table[@width = '940'][@bgcolor = '#666666'][1]//a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_17173(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='tabulaWhite']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//table/tr/td/span[@class='fel']/a/@href").extract())
        hxs_a.extend(hxs.select("//table/tbody/tr/td/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='NewsList4']/ul/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='content']//div[@class='newslist']/div[@class='showlist1']/ul/li/a/@href").extract())
        hxs_a.extend(hxs.select("//table[@class='cmswz']/tr/td/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='listFont']/ul/li/span/a/@href").extract())
        hxs_a.extend(hxs.select("//tr/td/div[@class='list5']/ul/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='main']//div[@class='bd']/ul/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_ali213(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='liebyj_lei']/div[@class='liebyj_lei11']//div[@class='liebyj_lei3' or @class='liebyj_lei41']/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='newbiao']//div[@class='newbiao_la']/ul/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='cbox']/div[@class='box_left']/ul/li/span/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='box_left']//span[@class='left']/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id='newbiao_la']//li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_gamersky(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table/tr/td[@class='dlist']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_163(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='content']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='sublists']/ul[@class='f14bla sublist cWhite']/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='maincon']/ul[@class='lst-dot']/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_pcgames(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='artList']/ul/li/div[@class='dTitle']/b/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sc2p(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='NewsColumn1']//div[@class='NewsList DataList']/table/tr/td[@class='col1']/div/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_uuu9(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='news_top_bg']/li/a/@href").extract()
        hxs_a.extend(hxs.select("//ul[@class='textlist f_14']//li[@class = 't']/a/@href").extract())
        hxs_a.extend(hxs.select("//ul[@class='textlist f_14']//li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_tgbus(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table/tr/td[@class='STYLE15']/a[@title]/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='hide']/div[@class='list']//b/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='rk_content']//li[@class = 't']/a/@href").extract())
        if not hxs_a:
            hxs_a = hxs.select("//h2[@class = 'title']/a/@href").extract()
        if not hxs_a:
            hxs_a = hxs.select("//li[@class = 't']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_178(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='list-main']/div[@class='news-list clearfix']/ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_diablo3(self, response):
        '''超玩--暗黑3'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//span[@class='Level0']/a/@href").extract()

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
        item['sum_mark'] = meta['mission'][3].strip()
        item['child_mark'] = meta['mission'][4].strip()

        return item
