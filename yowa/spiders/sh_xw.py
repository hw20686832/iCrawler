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

class sh_xw_Spider(CrawlSpider):
    name = 'sh_xw'
    
    def start_requests(self):
        missions = session.getMission(sum_mark = 'xw', child_mark = 'sh')
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


    def parse_41go(self, response):
        '''试衣网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//h6/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_shop67(self,response):
        ''' 伊人服饰搭配网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'L2']//li//a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_sportica(self,response):
        '''斯波帝卡'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'news-ls-box']//a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_yokamen(self,response):
        '''YOKA男士网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'row1lf']/dl/dd//a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_meishij(self,response):
        '''美食杰'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'lp_result_list']//li/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_meishichina(self,response):
        '''美食天下'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'tList2']//li/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_tumanduo(self,response):
        '''装修图满多'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//dl[@class = 'uInfo']/dd/span/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_rayli(self,response):
        '''瑞丽家居'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'contleftxiatitle01 txt1']/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_china(self, response):
        '''地产中国网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='spxw_left']/a[contains(@href,'/')]/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_taofang(self, response):
        '''淘房网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@valign='middle']/a[contains(@href,'newsinfo.asp?newsid=')]/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_familydoctor(self, response):
        '''家庭医生在线'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'content']//ul[@class='textList']//i[@class='iTitle']/a/@href").extract()
        hxs_a.extend(hxs.select("//ul[@class='list_ny']/li/a/@href").extract())
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_39(self, response):
        '''39健康网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'listbox']//li/span[@class = 'text']/a/@href").extract()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_intopet(self, response):
        '''走进猫咪网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//a[@class = 'tbg30A']/@href").extract()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_ttpet(self, response):
        '''天天宠物网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class = 'mid_content gry_link2']/li//a/@href").extract()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_aigou(self, response):
        '''爱狗网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//h3/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_iyanghua(self, response):
        '''爱养花'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id = 'LisCnt']//a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_yuhuagu(self, response):
        '''沐花谷花卉网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class = 'e2']//a[@class='title']/@href").extract()

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
            
    def parse_autohome(self, response):
        '''汽车之家'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id = 'ArticlesTitles']//a[@id= 'ATitle']/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_gaibar(self, response):
        '''改吧'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//tr[@bgcolor = '#f5f5f5']//a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_zsku(self, response):
        '''百科知识库'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@class = 'shoplistrow']//a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_muqin(self, response):
        '''中国母亲网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table//a[@class = 'links1']/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_beva(self, response):
        '''贝瓦网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//a[@class = 'ltitle']/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_tongnian(self, response):
        '''童年网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//dl[@class = 'bbda cl']//a[@class = 'xi2']/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_jkyd(self, response):
        '''健康有道网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//span[@style = 'font-size: 14px']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_sina(self, response):
        '''新浪'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//h2/a/@href").extract()
        hxs_a.extend(hxs.select("//li/a/@href").extract())
        hxs_a.extend(hxs.select("//span[@class = 'c_tit']/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_sohu(self, response):
        '''搜狐'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'f14list']//a/@href").extract()
        hxs_a.extend(hxs.select("//a[@test='a']/@href").extract())
#        hxs_a.extend(hxs.select("//a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_qq(self, response):
        '''腾讯'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'mod newslist']//a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class = 'leftList']//li//a/@href").extract())
        hxs_a.extend(hxs.select("//div[@id = 'articleList']//li//a/@href").extract())
        hxs_a.extend(hxs.select("//a[@class='fs14']/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_163(self, response):
        '''网易'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'clearfix']//a/@href").extract()
        hxs_a.extend(hxs.select("//ul[@class = 'articleList']/li//a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class = 'content']//li//a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_ifeng(self, response):
        '''凤凰'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class = 'newsList']//ul/li//a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_lzyysw(self, response):
        '''老中医养身网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//cite/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_zhzyw(self, response):
        '''中华中医网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='ullist01']//li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_zhugou(self, response):
        '''助购网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table[@id='table']//td/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_bendibao(self, response):
        '''本地宝'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='fleft']/a[contains(@href,'bendibao')]/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_cocoren(self, response):
        '''爱尚网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@id='List_TextA']/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_szhk(self, response):
        '''深港在线'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@class='sznews_list']/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_marry52(self, response):
        '''美丽婚嫁'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='listtitle']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_99wed(self, response):
        '''久久结婚'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='news_lb_cons_ul right']//li//a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_gongyishibao(self, response):
        '''公益时报'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='class_list']//ul/li//a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_huishua(self, response):
        '''惠刷网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id='ll']//a[@class = 'f']/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_nfqs(self, response):
        '''国家食品质量安全网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//a[@class='hui']/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_china12315(self, response):
        '''食品安全快速检测'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//ul[@id='yf_2_2ul']//a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
                        
    def parse_xiumei(self, response):
        '''秀美网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//h4/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_gov(self, response):
        '''中国农业信息网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//a[@class='link03']/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='zleft']//li//a/@href").extract())
        
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
