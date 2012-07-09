import time

from scrapy.utils.request import request_fingerprint
from scrapy.exceptions import IgnoreRequest
from scrapy.dupefilter import BaseDupeFilter

from yowa.utils import cs

class RedisDupeFilter(BaseDupeFilter):
    def request_seen(self, request):
        if request.meta.has_key('spider'):
            spider = request.meta['spider']
            mission = request.meta.get('mission', ('', ''))
            seen = '#'.join((mission[1], request.url))

            if cs.zscore('crawled_url_%s' % spider, seen):
                cs.zadd('crawled_url_%s' % spider, seen, time.time())
                return True
