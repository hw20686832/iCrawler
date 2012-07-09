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

class CJ_XW_Spider(CrawlSpider):
    name = 'cj_xw'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'xw', child_mark = 'cj')
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
        hxs_a = hxs.select("//ul[@class='list_009']/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='main']/table/tr/td[@class='tal f14']/a/@href").extract())
        hxs_a.extend(hxs.select("//table[@class='body_table']/tbody/tr/th/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='content']/ul/li//a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_163(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='colLM']/ul/li/span/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_qq(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='main']/div[@class='mod newslist']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@id='tablelsw']/table/tr/td/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sohu(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='main area']/div[@class='lc']/div[@class='f14list']/ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_eastmoney(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='mainFrame']//div[@class='listBox']/div[@class='list']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='areacont blueline notopline mainlist']/div[@class='ztlist']/ul/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='newlistBox']/div[@class='list']/ul/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_hexun(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='mainboxcontent']//div[@class='temp01' or @class='list24px']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//table[@class='tableCont']/tbody/tr/td[@class='title']/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='stockul']/div/ul[@class='tempul']/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='mainbox']/ul[@class='inflist']/li/a[2]/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_dyhjw(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='sidebox']/div[@class='slist']/ul/li/span/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='sidebox']/div[@class='slist']/ul/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_cnfol(self, response):
        '''中金在线'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='BdPiL L']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='content l30']/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_sssc(self, response):
        '''盛世收藏'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='def14_tit clearfix']//a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_socang(self, response):
        '''中国收藏网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//li[@class='if_font2']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_zisha123(self, response):
        ''' 紫砂之家'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='box_row']//li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_baiyintouzi(self, response):
        ''' 白银投资'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='nr a14px']/ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_silver(self, response):
        ''' 第一白银网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='lb_you left']/div[@class = 'nr']/ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_shbyw(self, response):
        ''' 上海白银网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='articlelist']/ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_cngold(self, response):
        ''' 中国黄金投资网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='list_left']/ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_24goldzone(self, response):
        ''' 中国黄金白银网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='my_list']/ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_godsignal(self, response):
        ''' 白银投资策略网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='list_left_main']/ul//li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_jxtzw(self, response):
        ''' 金银家策略投资网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//dt[@class='xs2']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_cs(self, response):
        '''  中国证券报'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='z_list']//a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_stcn(self, response):
        '''  证券时报网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='mainlist']//a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_cnstock(self, response):
        '''  中国证券网'''
        if 'xml' in response.url:
            xxs = XmlXPathSelector(response)
                        
            hxs_a = xxs.select("//Item/@href").extract()
            for a in hxs_a:
                if not a.startswith('http'):
                    base_url = get_base_url(response)
                    a = urljoin_rfc(base_url, a)
    
                yield Request(url = a, meta = response.meta, callback = self.parse_item)
        else:
            hxs = HtmlXPathSelector(response)
            url1 = response.url
            url2 = hxs.select("//sslabel/@xmlurl").extract()
            if url2:
                url = url1 +url2[0]
                yield Request(url = url, meta = response.meta, callback = self.parse_cnstock)
        
    def parse_jrj(self, response):
        '''  金融界'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='ls1']/li//a/@href").extract()
        hxs_a.extend(hxs.select("//ul[@class='tab jrj-f14']/li/a//@href").extract())
        hxs_a.extend(hxs.select("//div[@class='wl']//li/a//@href").extract())
        hxs_a.extend(hxs.select("//ul[@class='ull']/li/a/@href").extract())
        hxs_a.extend(hxs.select("//ul[@class='jrj-l1']/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_ccstock(self, response):
        '''  证券日报'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@class='titleclass']//a/@href").extract()
        
        meta['release_time'] = hxs.select("//span[@class = 'daohang']/text()").extract()[0]
        r = re.compile(u"(20\d\d.*日)")
        meta['release_time'] = r.search(meta['release_time']).group()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = meta, callback = self.parse_item)
            
    def parse_sse(self, response):
        '''  上海证券交易所'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@class='content']/a/@onclick").extract()
        
        meta['title'] = hxs.select("//td[@class='content'][@height = '24']/a/text()").extract()
        meta['release_time'] = hxs.select("//span[@class='date']/text()").extract()
        num = 0;
        for a in hxs_a:
            a = a.replace("sse_popup('","")
            a = a.replace("')","")
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1
            yield Request(url = a, meta = meta, callback = self.parse_item)
            
    def parse_szse(self, response):
        '''  深圳证券交易所'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@class='td2']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_newone(self, response):
        '''  招商证券'''
        meta = response.meta
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@id='maincontainer']//a/@href").extract()
        if not hxs_a:
            hxs_a = hxs.select("//td[@id='td5']//li//a/@href").extract()
        meta['release_time'] = hxs.select("//td[@id='td5']//li/em/text()").extract()
        
        num = 0
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            meta['num'] = num
            num = num +1
            yield Request(url = a, meta = meta, callback = self.parse_item)
            
    def parse_quamnet(self, response):
        '''  华富财经'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@valign='top']/a[@class = 'content_lt_blue_link']/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_fx168(self, response):
        '''  fx168外汇宝'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//a[contains(@id,'DataList1')]/@href").extract()
        hxs_a.extend(hxs.select("//table[@id = 'DataList1']//a/@href").extract())
        if not hxs_a:
            hxs_a = hxs.select("//p[@class = 'P10L']/a[@class = 'index2']/@href").extract()
            hxs_a.extend(hxs.select("//font[@face = 'Arial']/a[@class = 'index2']/@href").extract())
            hxs_a.extend(hxs.select("//p[@class = 'P10']/a[@class = 'index2']/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_qhrb(self, response):
        '''  期货日报网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='list_news']//a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
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
            
    def parse_cctvcj(self, response):
        '''  CCTV-财经新闻'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='dynamic']/ul/li/a/@href").extract()
        if not hxs_a:
            hxs_a = hxs.select("//div[@class = 'box_news']//ul[@class = 'text_list']//a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_stockstar(self, response):
        '''  证券之星'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='list-line']/li/a/@href").extract()
        if not hxs_a:
            hxs_a = hxs.select("//div[@class = 'listnews']//a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_cfi(self, response):
        '''  中财网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//a[@style='color:balck;font-size:10.8pt;']/@href").extract()
        if not hxs_a:
            hxs_a = hxs.select("//a[@class = 'title']/@href").extract()

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
        
        if 'sse.com.cn' in url:
            item['title'] = meta['title'][meta['num']]
            item['release_time'] = meta['release_time'][meta['num']]
            
        if 'ccstock.cn' in url:
            item['release_time'] = meta['release_time']
            
        if '/researchcontroller/' in url:
            item['release_time'] = meta['release_time'][meta['num']]
        return item
