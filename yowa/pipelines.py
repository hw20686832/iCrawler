# coding: utf-8
import subprocess
import time, datetime
import json
import re

from pyquery import PyQuery
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from scrapy import log
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.conf import settings

from yowa.utils import cs
from yowa.items import *

class YowaPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url, headers = {'Referer': image_url})

    def item_completed(self, results, item, info):

        spider = info.spider
        seen = '#'.join((item['father_url_number'], item['child_url']))
        if cs.zscore('crawled_url_%s' % spider.name, seen):
            raise DropItem("Duplicate item found: %s" % item)

        content = item['content']
        content_html = PyQuery(content)

        content_link = content_html('a')
        
        content_a = []

        if 'xw' in item['sum_mark'] or 'jr' in item['sum_mark']:
            #delete the <a
            content_html = content_html.html()
            alink1 = re.compile(u'<a.*?>')
            content_html = alink1.sub('',content_html)
            
            alink2 = re.compile(u'<\/a>')
            content_html = alink2.sub('',content_html)
            
            
            #delete the color
            content_html = PyQuery(content_html)
                    
            content_style = content_html('[style]')
            for style_d in content_style:
                if 'color' in content_style.eq(content_style.index(style_d)).attr('style') or 'COLOR' in content_style.eq(content_style.index(style_d)).attr('style'):
                    content_style.eq(content_style.index(style_d)).removeAttr('style')
            
            content_color = content_html('[color]')
            for color_d in content_color:
                    content_color.eq(content_color.index(color_d)).removeAttr('color')
            
        #delete the width height         
        img_d = content_html('img')
        for img in img_d:
            if not img.get('src'):
                continue
            elif '.gif' in img.get('src'):
                continue
            else:
                if img_d.eq(img_d.index(img)).attr('width'):
                    img_d.eq(img_d.index(img)).removeAttr('width')
                if img_d.eq(img_d.index(img)).attr('height'):
                    img_d.eq(img_d.index(img)).removeAttr('height')
                if img_d.eq(img_d.index(img)).attr('style'):
                    img_d.eq(img_d.index(img)).removeAttr('style')
        
        #delete the table width
        table_d = content_html('table')
        for tab in table_d:
            if table_d.eq(table_d.index(tab)).attr('width'):
                    table_d.eq(table_d.index(tab)).removeAttr('width')

        #delete the font center 
        div_d = content_html('div')
        for div in div_d:
            if div_d.eq(div_d.index(div)).attr('align'):
                    div_d.eq(div_d.index(div)).removeAttr('align')
        p_d = content_html('p')
        for p in p_d:
            if p_d.eq(p_d.index(p)).attr('style'):
                    p_d.eq(p_d.index(p)).removeAttr('style')
        #delete the link font
        link_d = content_html('link')
        for rel in link_d:
            if link_d.eq(link_d.index(rel)).attr('rel'):
                    link_d.eq(link_d.index(rel)).removeAttr('rel')
                    
        #delete the font strong
        content_html = content_html.html()
        strong1 = re.compile(u'<strong.*?>')
        content_html = strong1.sub('',content_html)
        
        strong2 = re.compile(u'<\/strong>')
        content_html = strong2.sub('',content_html)
        
        #delete the font
        font1 = re.compile(u'<font.*?>')
        content_html = font1.sub('',content_html)
        
        font2 = re.compile(u'<\/font>')
        content_html = font2.sub('',content_html)
        
        #delete the pre
        pre1 = re.compile(u'<pre.*?>')
        pre2 = re.compile(u'</pre>')
        pre3 = re.compile(u'<pre/>')
        
        content_html = pre1.sub('',content_html)
        content_html = pre2.sub('',content_html)
        content_html = pre3.sub('',content_html)

        #delete the center
        center1 = re.compile(u'<center.*?>')
        center2 = re.compile(u'</center>')
        center3 = re.compile(u'<center/>')
        
        content_html = center1.sub('',content_html)
        content_html = center2.sub('',content_html)
        content_html = center3.sub('',content_html)
        
        #delete the image background
        backg1 = re.compile(u'style="height:1px"')
        content_html = backg1.sub('',content_html)
        content_html = PyQuery(content_html)      

        # the center
        imgn = 1      
        img_d2 = content_html('img')
        for img in img_d2:
            if not img.get('src'):
                continue
            elif '.gif' in img.get('src'):
                continue
            elif '.GIF' in img.get('src'):
                continue
            else:
                if 'wb' not in item['sum_mark']:
                    img_d2.eq(img_d2.index(img)).wrap('<a href="woshi'+str(imgn)+'hao"><p align="center"></p></a>')
                    imgn = imgn+1
                else:
                    img_d2.eq(img_d2.index(img)).wrap('<p align="center"></p>')
                    imgn = imgn+1

                    
        # replace the img_url   
        n = 0
        img_d3 = content_html('img')
        for img in img_d3:
            if not img.get('src'):
                continue
            elif '.gif' in img.get('src'):
                n = n+1
                continue
            elif '.GIF' in img.get('src'):
                n = n+1
                continue
            else:
                if 'http' in img.get('src'):
                    continue
                else:
                    content = content_html.html()
                    content = content.replace(img.get('src'),item['image_urls'][img_d3.index(img)-n])
                    content_html = PyQuery(content)
        
        content = content_html.html()
        image_paths = [x['path'] for ok, x in results if ok]

        image_interval = settings.get('IMAGES_INTERVAL')
        def sub_image(thumb, full):
            pattern = re.compile('full/(.*?)\.jpg')
            path = pattern.sub('/images/%s/\\1.jpg?d=%s' % (thumb, image_interval), full)
            return path
        
        img_number = 1
        for ok, x in results:
            if ok:
                path = sub_image('thumbs/big', x['path'])
                full_path = sub_image('full', x['path'])
                content = content.replace('&amp;', '&')
                
                img_yuan = "woshi" +str(img_number)+ "hao"
                content = content.replace(img_yuan, full_path)
                content = content.replace(x['url'], path)
                img_number = img_number+1
        
        if not item['pic_url']:
            item['pic_url'] = sub_image('thumbs/small', image_paths[0]) if image_paths else None
            
        content_text = PyQuery(content)
        cont_text = content_text.text()
        if not cont_text:
            raise DropItem("This content is NULL: %s" % item['child_url'])
        item['content'] = content
        item['climb_time'] = time.time()

        jitem = json.dumps(item.withdict())
        cs.rpush('data_%s' % spider.name, jitem)
        cs.zadd('crawled_url_%s' % spider.name, seen, time.time())

        return item

class DaemonPipeline(object):
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        from yowa.db import session
        while cs.llen('data_%s' % spider.name):
            jitem = cs.lpop('data_%s' % spider.name)
            item = json.loads(jitem)
            try:
                session.addContent(item)
                log.msg("Insert to DB: [%s, %s, %s]" % (item['father_url_number'], item['child_url'], item['title']), level=log.INFO)
            except Exception, e:
                cs.rpush('error_data_%s' % spider.name, jitem)
                log.msg("Some error happend on insert row: [%s, %s, %s], error message: %s" % (item['father_url_number'], item['child_url'], item['title'], str(e)), level=log.WARNING)

        month_ago = time.mktime((datetime.datetime.now() + datetime.timedelta(days = -30)).timetuple())
        cs.zremrangebyscore('crawled_url_%s' % spider.name, '-inf', month_ago)
        session.close()
