# coding: utf-8
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.exceptions import NotSupported, DropItem

from yowa.utils import urltools
from yowa.utils import ParserManager

class YowaSpider(BaseSpider):
    name = None
    missions = []

    def getRealURI(self, u, response):
        uri = u
        if not uri.startswith('http'):
            base_url = get_base_url(response)
            uri = urljoin_rfc(base_url, uri)

        return uri

    def start_requests(self):
        for m in self.missions:
            try:
                meta = {'spider': self.name,
                        'domain': urltools.get_domain(m[0]),
                        'mission': m}

                yield Request(url = m[0],
                              meta = meta,
                              callback = self.__getattribute__('parse_%s' % meta['domain']))
            except:
                continue

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
            
