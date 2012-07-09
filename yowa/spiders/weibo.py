# coding: utf-8
import re, time
import json

from pyquery import PyQuery

from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.xlib import BeautifulSoup
import BeautifulSoup  
from scrapy.contrib.spiders import CrawlSpider
from scrapy.conf import settings

from yowa.items import ContentItem
from yowa.db import session

class WeiboSpider(CrawlSpider):
    name = 'all_wb'

    def start_requests(self):
        missions = session.getMission(sum_mark = 'wb')
        for m in missions:
            meta = {'mission': m}
            if 'weibo.com' in m[0]:
                parse_back = self.parse_sina
            else:
                parse_back = self.parse_qq

            yield Request(url = m[0],
                          meta = meta,
                          callback = parse_back)
        
    def parse_sina(self, response):
        hxs = HtmlXPathSelector(response)
        face_a = hxs.select("//a[@class='face' and @title]")
        pname = face_a.select("./@title").extract()[0]
        pic_url = face_a.select("./img/@src").extract()[0]

        hxs_script = hxs.select('//script[contains(text(), "pl_content_unlogin_profilefeed")]').extract()
        script = re.findall('<script>STK && STK\.pageletM && STK\.pageletM\.view\((.*?)\)</script>', hxs_script[0])[0]
        html = json.loads(script).get('html')
#        soup = BeautifulSoup.BeautifulSoup(html)
        doc = PyQuery(html)
        dls = doc("dl[action-type = 'feed_list_item']")
#        dls = soup.findAll('dl', {'action-type': 'feed_list_item'})

        for dl in dls:
            item = ContentItem()
            item['father_url_number'] = response.meta['mission'][1]
            item['title'] = dls.eq(dls.index(dl)).find("p[node-type = 'feed_list_content']").text()
            if not item['title']:
                item['title'] = u'[图片]'
            forward = dls.eq(dls.index(dl)).find("dt[node-type = 'feed_list_forwardContent']")
            forward_media = dls.eq(dls.index(dl)).find("dd[node-type = 'feed_list_media_prev']")
            if forward:
                if forward_media:
                    content = dls.eq(dls.index(dl)).find("p[node-type = 'feed_list_content']").html()+'<br />'.join([forward.html(), forward_media.html()])
                else:
                    content = dls.eq(dls.index(dl)).find("p[node-type = 'feed_list_content']").html()+'<br>'+forward.html()
            else:
                if dls.eq(dls.index(dl)).find("ul[class = 'piclist']").html():
                    content = dls.eq(dls.index(dl)).find("p[node-type = 'feed_list_content']").html()+dls.eq(dls.index(dl)).find("ul[class = 'piclist']").html()
                else:
                    content = dls.eq(dls.index(dl)).find("p[node-type = 'feed_list_content']").html()
            item['content'] = content
            item['source'] = u'新浪微博'
            rtime = dls.eq(dls.index(dl)).find("p[class = 'info W_linkb W_textb']")
            item['release_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(rtime.find("a[node-type = 'feed_list_item_date']").attr('date'))/1000))
            item['child_url'] = '#'.join([response.url, dl.get('mid')])
            item['author'] = pname
            item['pic_url'] = pic_url
            item['sum_mark'] = response.meta['mission'][3]
            item['child_mark'] = response.meta['mission'][4]
            item['image_urls'] = []
            
            yield item

    def parse_qq(self, response):
        meta = response.meta
        doc = PyQuery(response.body)

        pic_url = doc('div.main')('li.pic')('img').attr('src')
        pname = doc('li.detail')('h4')('span.userName').text()

        lis = doc('ul#talkList')('li')
        for li in lis:
            item = ContentItem()
            item['father_url_number'] = meta['mission'][1]
            item['title'] = lis.eq(lis.index(li))('div.msgCnt').eq(0).text()
            if not item['title']:
                item['title'] = u'[图片]'
            content1 = lis.eq(lis.index(li))('div.msgCnt').eq(0)
            content1.remove('div.pubInfo')
            content2 = lis.eq(lis.index(li))('div.msgBox').eq(1)
            content2.remove('div.pubInfo')
            content = content1.__unicode__()+lis.eq(lis.index(li))('div.mediaWrap').eq(0).__unicode__()+'<br>'+content2.__unicode__()
            content = content.replace('crs=','src=')
            item['content'] = content
            item['source'] = u'腾讯微博'
            item['release_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(li.get('rel'))))
            item['child_url'] = '#'.join([response.url, li.get('id')])
            item['author'] = pname
            item['pic_url'] = pic_url
            item['sum_mark'] = response.meta['mission'][3]
            item['child_mark'] = response.meta['mission'][4]
            item['image_urls'] = []

            yield item
