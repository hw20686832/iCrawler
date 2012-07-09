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

class DiscussionSpider(CrawlSpider):
    name = 'all_tz'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'tz')
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
        hxs_a = hxs.select("//div[@class='threadlist datalist']/form/table/tbody[contains(@id, 'normalthread_')]//span[contains(@id, 'thread_')]/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='mainbox threadlist']/form/table/tbody[contains(@id, 'normalthread_')]/tr/td[@class='folder']/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='blk_tb_01']/table/tr/td/a[1]/@href").extract())
        hxs_a.extend(hxs.select("//table[contains(@id,'forum_')]/tbody[contains(@id, 'normalthread_')]/tr[@class='test']/th/span[contains(@id, 'thread_')]/a/@href").extract())
        hxs_a.extend(hxs.select("//span[contains(@id,'thread_')]//a[contains(@href,'.html')]/@href").extract())
        
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sohu(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//table/tr[contains(@class, "blueBorder")]/td/span[contains(@class, "f14")]//a[contains(@href, "%s")]/@href' % urlparse.urlparse(response.url).hostname).extract()
        hxs_a.extend(hxs.select('//div[@id="threadlist"]//tbody[contains(@id, "normalthread_")]/tr/td[@class="folder"]/a/@href').extract())
        hxs_a.extend(hxs.select("//div[@class='f14list']//a/@href").extract())
        hxs_a.extend(hxs.select("//tr[contains(@class, 'blueBorder')]/td/span[contains(@class, 'f14')]/a/@href").extract())
        
        meta = response.meta
        meta['simulate'] = True
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = meta, callback = self.parse_item)

    def parse_163(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='bm_c']/form/table/tbody[contains(@id, 'normalthread_')]/tr/td[@class='num']/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='articleItem' or @class='articleItem odd']/span[@class='s1']/a/@href").extract())
        hxs_a.extend(hxs.select("//table[@class='uc_bbs_list']/tr[@topType='0']/td[@class='uc_bbs_title']/a/@href").extract())
        hxs_a.extend(hxs.select("//td[@class = 'uc_bbs_title']/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_qq(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//tbody[contains(@id, "normalthread_")]//td[@class="icn"]/a/@href').extract()
        hxs_a.extend(hxs.select("//span[contains(@id,'thread_')]/a/@href").extract())
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_67(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//div[@class="threadlist"]//td[@class="folder"]/a/@href').extract()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)
    
    def parse_hexun(self, response):
        hxs = HtmlXPathSelector(response)
#        hxs_a = hxs.select('//div[@class="gcon_2"]/table//div[@class="t"]/a[@class="f14"]/@href | //div[@id="topiclist"]/dl[not(@class)]/dt/a/@href').extract()
        hxs_a = hxs.select("//div[@id='topiclist']/dl/dt//a[1]/@href").extract()
        hxs_a.extend(hxs.select("//table[@class='bbslist']/tr[@class='bg']/td[@class='f14']/a/@href").extract())
        hxs_a.extend(hxs.select("//div[@class='blk_tb_01']/table[@class='tb_01']/tr/td/a[1]/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_eastmoney(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//div[@class="lileft"]/a[@class="link_blue"]/@href').extract()
        hxs_a.extend(hxs.select("//div[@class='h4' or @class='h3']/ul/li[@class='l3']/a[not(@class)]/@href").extract())
        rc = re.compile(r"document\.write \(dvbbs_topic_list\(TempStr,'(.*?)','(.*?)',.*?\)\);")
        rrc = rc.findall(response.body)
        urls = []
        for id, bid in rrc:
            urls.append('/dispbbs.asp?boardID=%s&ID=%s&page=1' % (bid, id))
        hxs_a.extend(urls)

        meta = response.meta
        meta['simulate'] = True
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = meta, callback = self.parse_item)

    def parse_eastday(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//tbody[contains(@id, 'normalthread_')]/tr/td[@class='folder']/a/@href").extract()
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_zol(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//div[@class="Dm_3 mt8"]//a[@class="lan14i" and @title]/@href').extract()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_pconline(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//div[@class="list_com"]//dd/span[@class="sp1"]/a/@href').extract()
        hxs_a.extend(hxs.select("//div[@id='blockD']/div[@class='tb']/table//em/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_yesky(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//div[@class="main"]//div[@class="list"]/ul/li/a[not(@class)]/@href').extract()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_it168(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//tbody[contains(@id, "stickthread_")]//th[@class="common"]/a/@href').extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_ngacn(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//table[@id="topicrows"]/tbody/tr[contains(@class, "topicrow")]/td[@class="c1"]/a/@href').extract()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sgamer(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//div[@class="bm_c"]//tbody[contains(@id, "stickthread_")]/tr/td/a/@href').extract()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_plu(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//div[@id="threadlist"]//tbody[contains(@id, "normalthread_")]/tr/td[@class="folder"]/a/@href').extract()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_replays(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='bm_c']/form/table/tbody[contains(@id, 'normalthread_')]/tr/td[@class='num']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_winning11cn(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//div[@id="threadlist"]//tbody[contains(@id, "normalthread_")]/tr/td[@class="folder"]/a/@href').extract()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_duowan(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='bd']/form/table/tbody[contains(@id, 'normalthread_')]/tr/td[@class='folder']/a/@href").extract()
        hxs_a.extend(hxs.select("//tbody[contains(@id,'normalthread')]//span[contains(@id,'thread_')]/a/@href").extract())
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_17173(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='bbsTopicsListAll']/table/tbody/tr/td[@align='center'][1]/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_ali213(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='forum_line_padding']/form/table/tbody[contains(@id, 'normalthread_')]/tr/td[@class='icn']/a/@href").extract()
        hxs_a.extend(hxs.select("//div[@class='box_left']//span[@class='left']/a/@href").extract())
        hxs_a.extend(hxs.select("//tbody[contains(@id,'normalthread_')]//th[@class='new']/a[@class = 'xst']/@href").extract())
        
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_sc2(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='bd']/form/table/tbody[contains(@id, 'normalthread_')]/tr/td[@class='folder']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_uuu9(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//div[@id="threadlist"]//tbody[contains(@id, "normalthread_")]/tr/td[@class="folder"]/a/@href').extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_tgbus(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//div[@id="threadlist"]//tbody[contains(@id, "normalthread_")]/tr/td[@class="folder"]/a/@href').extract()
        hxs_a.extend(hxs.select("//div[@class='rk_content']//li[@class = 't']/a/@href").extract())
        if not hxs_a:
            hxs_a = hxs.select("//a[@class = 'xst']/@href").extract()
            
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_178(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='mainbox threadlist']/form/table/tbody[contains(@id, 'normalthread_')]/tr/td[@class='folder']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_ptbus(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='bm_c']/form/table/tbody[contains(@id, 'normalthread_')]/tr/td[@class='num']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_diaoyuweng(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='bm_c']/form/table/tbody[contains(@id, 'normalthread_')]/tr/td[@class='num']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_8264(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='bm_c']/form/table/tbody[contains(@id, 'normalthread_')]/tr/td[@class='num']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_tianya(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table[@class='listtable wbg' or @class='listtable bg']/tr/td[@class='posttitle faceblue']/a/@href").extract()
        hxs_a.extend(hxs.select("//table[@name='adsp_list_post_info_a' or @name='adsp_list_post_info_b']//td[2][not(@class='author')]/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_pcauto(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id='topic_list']/form/table/tbody/tr/th[@class='title']/span/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_autohome(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//table[@class='topicList ma_t2']/tbody/tr/td/a[@class='font14']/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_bitauto(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='postslist_xh']/ul/li[@class='tu']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_xcar(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//td[@class='line34']/a[@class='open_view']/@href").extract()
        hxs_a.extend(hxs.select("//ul[@class='pictxt_nt4']/li/a/@href").extract())

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_ifeng(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='main']//table/tr/td[@class='fz14']/a[1]/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_mop(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='content']//div[@class='jjP']/h3/a/@href").extract()
        hxs_a.extend(hxs.select("//tr[@data-sid]/td[contains(@class,'title')]//a[@title]/@href").extract()) 

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_douban(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id='content']//ul/li/h3/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)

    def parse_dyhjw(self, response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@id='threadlist']/form/table/tbody[contains(@id, 'normalthread_')]/tr/td[@class='folder']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_gamersky(self, response):
        '''������̳'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//span[contains(@id,'thread_')]/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_miercn(self, response):
        '''�׶���'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='wenzang']/div[@class = 'wenzang_titlel']/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_huanqiu(self, response):
        '''����'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//div[@class='section']//ul/li/a/@href").extract()

        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)

            yield Request(url = a, meta = response.meta, callback = self.parse_item)
            
    def parse_tiexue(self, response):
        '''��Ѫ��'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//h1[@class='h4Tile']/a/@href").extract()
        hxs_a.extend(hxs.select("//li[contains(@class,'picBg1')]/a[contains(@href,'http://bbs.tiexue.net/post2')]/@href").extract())

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
            
    def parse_dazhe021(self, response):
        '''上海打折网'''
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select("//tbody[contains(@id,'normalthread')]//th[@class = 'common']/a[@class = 'xst']/@href").extract()
        hxs_a.extend(hxs.select("//th[@class='new']//a[@class = 'xst']/@href").extract())
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

