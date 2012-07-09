from scrapy.http import Request, FormRequest, HtmlResponse

from yowa import settings
from yowa.utils import wk

class WebkitDownloader(object):
    def process_request(self, request, spider):
        if spider.name in settings.WEBKIT_DOWNLOADER:
            if(type(request) is not FormRequest and request.meta.has_key('simulate')):
                body = wk.run_webkit(request.url)
                return HtmlResponse(request.url, body = body)
            
