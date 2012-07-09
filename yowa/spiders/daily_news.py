# coding: utf-8
from scrapy.http import Request
from scrapy.exceptions import NotSupported, DropItem
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from yowa.utils import urltools
from yowa.utils import ParserManager

class DailyNews_Spider(CrawlSpider):
    name = 'daily_xw'
    start_urls = ['http://news.sohu.com/1/0903/61/subject212846158.shtml', 
                  'http://news.sohu.com/1/0903/62/subject212846267.shtml', 
                  'http://ent.sina.com.cn/star/mainland/more.html', 
                  'http://ent.sina.com.cn/star/hk_tw/more.html', 
                  'http://sports.sina.com.cn/scroll_top.shtml', 
                  'http://tech.qq.com/l/web/webnews/webnews.htm', 
                  'http://money.163.com/special/00252G50/macroNew.html',
                  'http://www.xinhuanet.com/jujiao.htm',
                  'http://news.ynet.com/2.1.0/76503.html',]

    def start_requests(self):
        for m in self.start_urls:
            try:
                meta = {'spider': self.name, 'domain': urltools.get_domain(m)}
                yield Request(url = m,
                              meta = meta,
                              callback = self.__getattribute__('parse_%s' % meta['domain']))
            except:
                continue


    def parse_sohu(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='lc']/div[@class='f14list']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='f14list']/ul/li/a[@rel='external']/@href").extract())
        hxs_a.extend(hxs.select("//td[@class='newsblue1']/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_gmw(self,response):
        ''' 光明网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table[@class = 'z14_01']/tbody/tr/td/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_jjckb(self,response):
        '''经济参考网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table[@class = 'tableblack_3']/tbody/tr/td/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_yahoo(self,response):
        '''雅虎'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'dbox']/div[@class = 'body']/ul[@class = 'list1']/li/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_people(self,response):
        '''人民网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class = 'dot_14']/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class = 'one_5 d2_15 d2tu_3 d2tu_4']/ul/li/a/@href").extract())
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_xinhuanet(self,response):
        '''新华网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@bgcolor = 'F5F9FC']/table/tr/td/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_qianlong(self,response):
        '''千龙网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id = 'more']/table/tr/td/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_ynet(self,response):
        '''北青网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'hc3 vb']/ul/li/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_sina(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='contList']//a/@href").extract()
        hxs_a.extend(hxs.select("//ul[@class='list_009']//a/@href").extract())
        hxs_a.extend(hxs.select("//td[@class='f149']//a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='d_list_txt']//span[@class = 'c_tit']/a/@href").extract())
        
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

    def parse_163(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='bd clearfix']//ul[@class='list-1 mb15']/li/a/@href").extract()
        hxs_a.extend(hxs.select("//ul[@class='articleList']/li/a/@href").extract())
        hxs_a.extend(hxs.select("//ul[@class='newsList dotted']/li/span/a/@href").extract())
        hxs_a.extend(hxs.select("//td[@class='newsblue1']/a/@href").extract())
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
        item['father_url_number'] = ''
        item['child_url'] = response.url
        item['sum_mark'] = 'jr'
        item['child_mark'] = 'jr'

        return item
