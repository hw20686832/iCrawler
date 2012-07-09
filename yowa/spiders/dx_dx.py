# coding: utf-8
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from yowa.items import ContentItem
from yowa.db import session
from yowa.utils import urltools

class DX_DX_Spider(CrawlSpider):
    name = 'dx_dx'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'dx', child_mark = 'dx')
        for m in missions:
            try:
                meta = {'mission': m, 'spider': self.name}
                yield Request(url = m[0],
                              meta = meta,
                              callback = self.__getattribute__('parse_%s' % urltools.get_domain(m[0])))
            except:
                continue

    def parse_sina(self, response):
        meta = response.meta
        hxs = HtmlXPathSelector(response)

        requests = []
        hxs_page = hxs.select("//form[@name='navigator2']/tr/td/a")
        
        for p in hxs_page:
            if p.select('./text()').extract()[0] == u'[下一页]':
                
                url = p.select('./@href').extract()[0]
                if not url.startswith('http'):
                    base_url = '/'.join(response.url.split('/')[:3])
                    url = urljoin_rfc(base_url, url)

                requests.append(Request(url = url, meta = meta, callback = self.parse_sina))

        hxs_a = hxs.select("//tbody/tr/td[@class='p3Itme1star']/a")
        for a in hxs_a:
            item = ContentItem()
            item['father_url_number'] = meta['mission'][1]
            item['child_url'] = a.select("./@href").extract()[0]
            item['title'] = a.select("./text()").extract()[0]
            item['content'] = a.select("./text()").extract()[0]
            item['sum_mark'] = meta['mission'][3]
            item['child_mark'] = meta['mission'][4]
            item['image_urls'] = []
            item['pic_url'] = ''
            requests.append(item)

        return requests
