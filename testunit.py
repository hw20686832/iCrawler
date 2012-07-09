#!/usr/bin/env python
# coding: utf-8
import sys
from optparse import OptionParser

from twisted.internet import reactor
from twisted.web import client
from scrapy.http import HtmlResponse

from yowa.utils import ParserManager, urltools

class Crawl:
    def __init__(self, url):
        self.url = url
        self.response = None
    
    def result(self, body):
        self.response = HtmlResponse(url = self.url, body = body)
        reactor.stop()
        
    def fetch(self):
        deferred = client.getPage(self.url)
        deferred.addCallback(self.result)
        
        reactor.run()

def run():
    parser = OptionParser()
    parser.add_option("-t", "--tpl", dest="template_name",
                  help="specified a template")
    parser.add_option("-u", "--url", dest="request_url", 
                  help="specified a request url as 'http://www.baidu.com/'")

    (options, args) = parser.parse_args()
    tpl = options.template_name
    url = options.request_url
    if not tpl or not url:
        sys.stderr.write("Type './testunit.py --help' for usage.\n")
        sys.exit(1)

    spider = Crawl(url)
    spider.fetch()

    pm = ParserManager(urltools.get_domain(url))
    p = pm.create(tpl, response = spider.response)
    item = p.extract()
    
    for kv in item.withdict().items():
        print u'[%s]: %s' % kv

if __name__ == '__main__':
    run()
