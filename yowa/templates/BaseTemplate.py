#coding: utf-8
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

class Base(object):
    name = None

    def __init__(self, response):
        self.response = response
        self.hxs = HtmlXPathSelector(response)
        self.html = response.body_as_unicode()
        self.title = ''
        self.content = ''
        self.release_time = ''
        self.source = ''
        self.author = ''
        self.pic_url = ''

    def extract(self):
        pass

    def getRealURI(self, u):
        uri = u
        if not uri.startswith('http'):
            base_url = get_base_url(self.response)
            uri = urljoin_rfc(base_url, uri)

        return uri
