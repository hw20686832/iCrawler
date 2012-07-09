'''
Created on 2011-12-27

@author: joyce
'''
# -*-encoding:utf-8-*-
import re
import json
import urlparse

from scrapy.http import Request
from scrapy.exceptions import NotSupported, DropItem
from scrapy.selector import HtmlXPathSelector
from scrapy.xlib import BeautifulSoup
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from yowa.items import ContentItem
from yowa.db import session
from yowa.utils import urltools
from yowa.utils import ParserManager

class LocalNewsSpider(CrawlSpider):
    name = 'bd_xw'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'xw', child_mark = 'bd')
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

    #=====gansudaily====
    def parse_gansudaily(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'span': {'class': ['auto_one', 't14_h']},
                          'td': {'class': ['zt14_h02']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                rs = soup.findAll(t, {p_t: p_p})
                if rs:
                    rs_url = rs[0].findAll('a',target='_blank')
                    for i in rs_url:
                        u = i['href']
                        if not u.startswith('http'):
                            base_url = get_base_url(response)
                            u = urljoin_rfc(base_url, u)
                            
                        yield Request(url = u, meta = response.meta, callback = self.parse_item)
                        
    #=====dbw=====
    def parse_dbw(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'div': {'class': ['newslist f14px','left w550 textleft f14px', 'black_12']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                rs = soup.findAll(t, {p_t: p_p})
                if rs:
                    rs_url = rs[0].findAll('a',target='_blank')
                    for i in rs_url:
                        u = i['href']
                        if not u.startswith('http'):
                            base_url = get_base_url(response)
                            u = urljoin_rfc(base_url, u)
                            
                        yield Request(url = u, meta = response.meta, callback = self.parse_item)
                       
    #=====chinanews=====
    def parse_chinanews(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'div': {'class': ['bm_c xld']},
                          'table':{'id':['ctl00_ContentPlaceHolder1_DataList1']},
                          'span':{'style':['FONT-SIZE: 14px; LINE-HEIGHT: 20pt']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                rs = soup.findAll(t, {p_t: p_p})
                if rs:
                    rs_url = rs[0].findAll('a')
                    for i in rs_url:
                        u = i['href']
                        if i.text == "":
                            continue
                        if not u.startswith('http'):
                            base_url = get_base_url(response)
                            u = urljoin_rfc(base_url, u)
                            
                        yield Request(url = u, meta = response.meta, callback = self.parse_item)
                        
    #=====qq=====
    def parse_qq(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'div': {'id':['listZone','PageSet','pContent'],
                                  'class':['mod newslist','leftList']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                rs = soup.findAll(t, {p_t: p_p})
                if rs:
                    rs_url = rs[0].findAll('a',target='_blank')
                    for i in rs_url:
                        u = i['href']
                        if not u.startswith('http'):
                            base_url = get_base_url(response)
                            u = urljoin_rfc(base_url, u)
                            
                        yield Request(url = u, meta = response.meta, callback = self.parse_item)
                        
    #=====ifeng=====
    def parse_ifeng(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'div': {'class':['newsList']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                rs = soup.findAll(t, {p_t: p_p})
                if rs:
                    rs_url = rs[0].findAll('a',target='_blank')
                    for i in rs_url:
                        u = i['href']
                        if not u.startswith('http'):
                            base_url = get_base_url(response)
                            u = urljoin_rfc(base_url, u)
                            
                        yield Request(url = u, meta = response.meta, callback = self.parse_item)

    #=====szhk=====
    def parse_szhk(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'ul': {'class':['sznews_list']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                    for rs in list:
                        url = rs.findAll('a',target='_blank')
                        for i in url:
                            u = i['href']
                            if not u.startswith('http'):
                                base_url = get_base_url(response)
                                u = urljoin_rfc(base_url, u)
                            
                            yield Request(url = u, meta = response.meta, callback = self.parse_item)
                   
    #=====daynews=====
    def parse_daynews(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'div': {'class':['area6_left2_box']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                rs = soup.findAll(t, {p_t: p_p})
                if rs:
                    rs_url = rs[0].findAll('a',target='_blank')
                    for i in rs_url:
                        u = i['href']
                        if not u.startswith('http'):
                            base_url = get_base_url(response)
                            u = urljoin_rfc(base_url, u)
                            
                        yield Request(url = u, meta = response.meta, callback = self.parse_item)
                                      
    #=====jxcn=====
    def parse_jxcn(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'div': {'class':['more1']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                rs = soup.findAll(t, {p_t: p_p})
                if rs:
                    rs_url = rs[0].findAll('a',target='_blank')
                    for i in rs_url:
                        u = i['href']     
                        if not u.startswith('http'):
                            base_url = get_base_url(response)
                            u = urljoin_rfc(base_url, u)
                            
                        yield Request(url = u, meta = response.meta, callback = self.parse_item)
                        
    #=====nxnews=====
    def parse_nxnews(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'td': {'class':['listblackf14h25']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                rs = soup.findAll(t, {p_t: p_p})
                if rs:
                    rs_url = rs[0].findAll('a',target='_blank')
                    for i in rs_url:
                        u = i['href']       
                        if not u.startswith('http'):
                            base_url = get_base_url(response)
                            u = urljoin_rfc(base_url, u)
                            
                        yield Request(url = u, meta = response.meta, callback = self.parse_item)
                        
    #=====bjd=====
    def parse_bjd(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'td': {'class':['outtd1']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                    for rs in list:
                        url = rs.findAll('a',target='_blank')
                        for i in url:
                            u = i['href']
                            if not u.startswith('http'):
                                base_url = get_base_url(response)
                                u = urljoin_rfc(base_url, u)
                            
                                yield Request(url = u, meta = response.meta, callback = self.parse_item)
       
    #=====99fang=====
    def parse_99fang(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'li': {'class':['info-title']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                    for rs in list:
                        url = rs.findAll('a',target='_blank')
                        for i in url:
                            u = i['href']
                            if not u.startswith('http'):
                                base_url = get_base_url(response)
                                u = urljoin_rfc(base_url, u)
                            
                            yield Request(url = u, meta = response.meta, callback = self.parse_item)
                            
    #=====17u=====
    def parse_17u(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'ul': {'class':['area_news']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                    for rs in list:
                        url = rs.findAll('a',target='_blank')
                        for i in url:
                            u = i['href']
                            if not u.startswith('http'):
                                base_url = get_base_url(response)
                                u = urljoin_rfc(base_url, u)
                            
                            yield Request(url = u, meta = response.meta, callback = self.parse_item)
                            
    #=====enorth=====
    def parse_enorth(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'tr': {'valign':['top']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                    for rs in list:
                        url = rs.findAll('a',target='_blank')
                        for i in url:
                            u = i['href']
                            if not u.startswith('http'):
                                base_url = get_base_url(response)
                                u = urljoin_rfc(base_url, u)
                            
                            yield Request(url = u, meta = response.meta, callback = self.parse_item)
                            
    #=====nmgnews=====
    def parse_nmgnews(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'ul': {'class':['f14bla','travel_list']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                    for rs in list:
                        url = rs.findAll('a',target='_blank')
                        for i in url:
                            u = i['href']
                            if not u.startswith('http'):
                                base_url = get_base_url(response)
                                u = urljoin_rfc(base_url, u)
                            
                            yield Request(url = u, meta = response.meta, callback = self.parse_item)
                            
    #=====jschina=====
    def parse_jschina(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'div': {'id':['NewsList']},
                  'td': {'class':['bian1']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                    for rs in list:
                        url = rs.findAll('a',target='_blank')
                        for i in url:
                            u = i['href']
                            if not u.startswith('http'):
                                base_url = get_base_url(response)
                                u = urljoin_rfc(base_url, u)
                            
                            yield Request(url = u, meta = response.meta, callback = self.parse_item)
                            
    #=====hiholiday=====
    def parse_hiholiday(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'table': {'bordercolorlight':['#FFFFCC']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                    for rs in list:
                        url = rs.findAll('a',target='_blank')
                        for i in url:
                            u = i['href']
                            if not u.startswith('http'):
                                base_url = get_base_url(response)
                                u = urljoin_rfc(base_url, u)
                            
                            yield Request(url = u, meta = response.meta, callback = self.parse_item)
                            
    #=====hinews=====
    def parse_hinews(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'div': {'class':['fl f14']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                    for rs in list:
                        url = rs.findAll('a',target='_blank')
                        for i in url:
                            u = i['href']
                            if not u.startswith('http'):
                                base_url = get_base_url(response)
                                u = urljoin_rfc(base_url, u)
                            
                            yield Request(url = u, meta = response.meta, callback = self.parse_item)
                            
    #=====gxnews=====
    def parse_gxnews(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'td': {'class':['fs14 li_disc','neiwen']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                   for rs in list:
                        url = rs.findAll('a')
                        for i in url:
                            u = i['href']
                            if not u.startswith('http'):
                                base_url = get_base_url(response)
                                u = urljoin_rfc(base_url, u)
                            
                            yield Request(url = u, meta = response.meta, callback = self.parse_item)
                            
    #=====gog=====
    def parse_gog(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'td': {'class':['font14']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                    for rs in list:
                        url = rs.findAll('a',target='_blank')
                        for i in url:
                            u = i['href']
                            if i.text == "":
                                continue
                            if not u.startswith('http'):
                                base_url = get_base_url(response)
                                u = urljoin_rfc(base_url, u)
                            
                            yield Request(url = u, meta = response.meta, callback = self.parse_item)
                            
    #=====chinatibetnews=====
    def parse_chinatibetnews(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'table': {'id':['nr_bj_id']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                    for rs in list:
                        url = rs.findAll('a',target='_blank')
                        for i in url:
                            u = i['href']
                            if not u.startswith('http'):
                                base_url = get_base_url(response)
                                u = urljoin_rfc(base_url, u)
                            
                            yield Request(url = u, meta = response.meta, callback = self.parse_item)
                            
    #=====yunnan=====
    def parse_yunnan(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'div': {'class':['layer2121','layer2723']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                    for rs in list:
                        url = rs.findAll('a')
                        for i in url:
                            u = i['href']
                            if not u.startswith('http'):
                                base_url = get_base_url(response)
                                u = urljoin_rfc(base_url, u)
                            
                            yield Request(url = u, meta = response.meta, callback = self.parse_item)
                            
    #=====tianshannet=====
    def parse_tianshannet(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'div': {'class':['title_txt','txt link05']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                    for rs in list:
                        url = rs.findAll('li')
                        if url:
                            for i in url:
                                rs_url = i.findAll('a')
                                for j in rs_url:
                                    u = j['href']
                                    if not u.startswith('http'):
                                        base_url = get_base_url(response)
                                        u = urljoin_rfc(base_url, u)
                            
                                    yield Request(url = u, meta = response.meta, callback = self.parse_item)
                        else:
                            rs_url = rs.findAll('a')
                            for i in rs_url:
                                u = i['href']
                                if not u.startswith('http'):
                                    base_url = get_base_url(response)
                                    u = urljoin_rfc(base_url, u)
                            
                                yield Request(url = u, meta = response.meta, callback = self.parse_item)
                                
    #=====qhnews=====
    def parse_qhnews(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'td': {'class':['hui13']},
                          'span': {'class':['hui12']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                    for rs in list:
                        url = rs.findAll('td',height='25')
                        if url:
                            for rs_url in url:
                                ulist = rs_url.findAll('a',target='_blank')
                                for i in ulist:
                                    u = i['href']
                                    if not u.startswith('http'):
                                        base_url = get_base_url(response)
                                        u = urljoin_rfc(base_url, u)
                            
                                    yield Request(url = u, meta = response.meta, callback = self.parse_item)
                                    
    #=====sdnews=====
    def parse_sdnews(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'div': {'class':['fl border LmAll']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                    for rs in list:
                        url = rs.findAll('ul')
                        for i in url:
                            rs_url = i.findAll('a')
                            for j in rs_url:
                                u = j['href']
                                if not u.startswith('http'):
                                    base_url = get_base_url(response)
                                    u = urljoin_rfc(base_url, u)
                            
                                yield Request(url = u, meta = response.meta, callback = self.parse_item)
                                
    #=====cheshi=====
    def parse_cheshi(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'div': {'class':['listboxp']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                    for rs in list:
                        url = rs.findAll('li')
                        for i in url:
                            rs_url = i.findAll('a')
                            for j in rs_url:
                                u = j['href']
                                if not u.startswith('http'):
                                    base_url = get_base_url(response)
                                    u = urljoin_rfc(base_url, u)
                            
                                yield Request(url = u, meta = response.meta, callback = self.parse_item)
                                
    #=====lotour=====
    def parse_lotour(self,response):
        soup = BeautifulSoup.BeautifulSoup(response.body)
        search_mapping = {'div': {'class':['elbox2']}}

        for t, p in search_mapping.items():
            for p_t, p_p in p.items():
                list = soup.findAll(t, {p_t: p_p})
                if list:
                    for rs in list:
                        url = rs.findAll('li')
                        for i in url:
                            rs_url = i.findAll('a')
                            for j in rs_url:
                                u = j['href']
                                if not u.startswith('http'):
                                    base_url = get_base_url(response)
                                    u = urljoin_rfc(base_url, u)
                            
                                yield Request(url = u, meta = response.meta, callback = self.parse_item)
                                
    #=====hebei=====
    def parse_hebei(self,response):
        hxs = HtmlXPathSelector(response)
        hxs_a = hxs.select('//div[@id="pContent"]//ul//li/a/@href').extract()
        for a in hxs_a:
            if not a.startswith('http'):
                base_url = get_base_url(response)
                a = urljoin_rfc(base_url, a)
            yield Request(url = a, meta = response.meta, callback = self.parse_item)
                  
        
    #=====sina=====  
    def parse_sina(self,response):
        base_url = urlparse.urlparse(response.url).hostname
        if base_url == "gd.news.sina.com.cn":
            soup = BeautifulSoup.BeautifulSoup(response.body)
            search_mapping = {'div': {'class':['list']}}

            for t, p in search_mapping.items():
                for p_t, p_p in p.items():
                    list = soup.findAll(t, {p_t: p_p})
                    if list:
                        for i in list:
                            rs_url = i.findAll('a',target='_blank')
                            for j in rs_url:
                                u = j['href']
                                if not u.startswith('http'):
                                    base_url = get_base_url(response)
                                    u = urljoin_rfc(base_url, u)
                                yield Request(url = u, meta = response.meta, callback = self.parse_item)            
        else:
            pattern = '\{"title":".*?","url":"(.*?)","createdate":".*?"\},'
            
            ob = re.compile(pattern)
            rs = ob.findall(response.body)
            for i in rs:
                if not i.startswith('http'):
                    base_u = get_base_url(response)
                    i = urljoin_rfc(base_u, i)
                yield Request(url = i, meta = response.meta, callback = self.parse_item)
        

    def parse_item(self, response):
        meta = response.meta
        try:
            pm = ParserManager(meta['domain'])
        except ImportError:
            raise NotSupported('Have no supported Template for domain: %s' % meta['domain'])

        item = {}
        match = False
        for tpl in pm.list():
            p = pm.create(tpl, response = response)
            try:
                item = p.extract()
                match = p.isMatch()
                if match:
                    break
            except Exception, e:
                continue

        if not match:
            raise DropItem('This page has not been extracted!')
        item['father_url_number'] = meta['mission'][1]
        item['child_url'] = response.url
        item['sum_mark'] = meta['mission'][3]
        item['child_mark'] = meta['mission'][4]

        return item
