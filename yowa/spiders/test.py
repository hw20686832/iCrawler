# coding: utf-8
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from yowa.spiders.yowaspider import YowaSpider
from yowa.db import session

class Test_Spider(YowaSpider):
    name = 'test'
    missions = session.getMission(child_mark = 'sz', sum_mark = 'xw')

    def parse_qq(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='main']/div[@class='mod newslist']/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='leftList']//ul/li/a/@href").extract())

        for a in hxs_a:
            yield Request(url = self.getRealURI(a, response), meta = response.meta, callback = self.parse_item)

    def parse_sina(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='list_009']/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='fixList']/ul/li/a/@href").extract())

        for a in hxs_a:
            yield Request(url = self.getRealURI(a, response), meta = response.meta, callback = self.parse_item)

    def parse_sohu(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@class='newsblue1']/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='f14list']/ul/li/a/@href").extract())

        for a in hxs_a:
            yield Request(url = self.getRealURI(a, response), meta = response.meta, callback = self.parse_item)

    def parse_163(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='bd clearfix']/div/ul/li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='content']/ul[@class='list_f14d']/li/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='bd clearfix']//ul[@class='list-1 mb15']/li/a/@href").extract())

        for a in hxs_a:
            yield Request(url = self.getRealURI(a, response), meta = response.meta, callback = self.parse_item)
            
    def parse_xilu(self, response):
        '''西陆网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='listbox']/dl//a/@href").extract()

        for a in hxs_a:
            yield Request(url = self.getRealURI(a, response), meta = response.meta, callback = self.parse_item)
            
    def parse_huanqiu(self, response):
        '''环球网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='section']//ul/li/a/@href").extract()

        for a in hxs_a:
            yield Request(url = self.getRealURI(a, response), meta = response.meta, callback = self.parse_item)
            
    def parse_people(self, response):
        '''人民网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='dot_14']//li/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='one_5 d2_15 d2tu_3 d2tu_4']/ul/li//a/@href").extract())

        for a in hxs_a:
            yield Request(url = self.getRealURI(a, response), meta = response.meta, callback = self.parse_item)
            
    def parse_qianlong(self, response):
        '''千龙网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id = 'more']//a/@href").extract()

        for a in hxs_a:
            yield Request(url = self.getRealURI(a, response), meta = response.meta, callback = self.parse_item)
            
    def parse_chinanews(self, response):
        '''中国新闻网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'dd_bt']/a/@href").extract()

        for a in hxs_a:
            yield Request(url = self.getRealURI(a, response), meta = response.meta, callback = self.parse_item)
