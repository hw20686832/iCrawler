#coding=utf-8
import re,os,sys

from pyquery import PyQuery
import Image
import urlparse

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'cenews'

    def extract(self):
        item = ContentItem()

        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('#tex')
        content_node.remove('style')
        (scheme, netloc, path, query) = urlparse.urlsplit(self.response.url)[:4]
        path = path[:path.rfind('/')]
        '''
        image_urls = [img.get('src') for img in content_node('img')]
        if type(path)==str:
            item['image_urls'] = [urlparse.urlunsplit((scheme, netloc, path+img.get('src'), query, '')) for img in content_node('img')]
        else:
            item['image_urls'] = [urlparse.urlunsplit((scheme, netloc, img.get('src'), query, '')) for img in content_node('img')]
        '''
        item['image_urls'] = [self.getRealURI(img.get('src')) for img in content_node('img') if not img.get('src').endswith('.gif')]
        item['title'] = self.title = doc('#title_tex').text()
        item['content'] = self.content = content_node.__unicode__()          
        item['release_time'] = self.release_time = doc('#time_tex').remove('span').eq(0).text()[:10]
        item['source'] = u'中国环境'
        item['author'] = ''
        item['pic_url'] = ''

        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False

def _urlclean(url):
    (scheme, netloc, path, query) = urlparse.urlsplit(url)[:4]
    return urlparse.urlunsplit((scheme, netloc, path, query, ''))