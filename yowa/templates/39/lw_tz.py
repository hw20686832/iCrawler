#coding: utf-8
'''
Created on 2012-3-8

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = '39_tz'

    def extract(self):
        item = ContentItem()
        self.html = re.sub('<!--.*?-->', '', self.html)
        
        title=self.hxs.select("//div[@class='tbrig']/h1/text()").extract()
        content=self.hxs.select("//div[@class='tbrig']").extract()
        tz_content=[]
        count=0
        all_content=''
        for con in content:
            doc=PyQuery(con)
            tz_content.append(doc('p'))
        for t_c in tz_content:
            if count==0:
                all_content=all_content+t_c.__unicode__()
                all_content=all_content+"<p>================</p>"
                count=count+1
            else:
                all_content=all_content+"<P>"+str(count)+" 楼<P>"
                all_content=all_content+t_c.__unicode__()
                all_content=all_content+"<p>-----------------</p>"
                count=count+1
                    
#        if not all_content:
#            content=self.hxs.select("//div[@class='tbrig']")[0].extract()
#            doc=PyQuery(content)
#            tz_content=doc('div.tbrig')
#            tz_content.remove('span')
#            tz_content=tz_content.__unicode__()
            
        
        tz_author=self.hxs.select("//div[@class='tblef']/span/a/text()").extract()
        release_time=self.hxs.select("//div[@class='tbrig']/span/b/text()").extract()
        ob=re.compile(u'20\d\d.*\d\d')
        release_time=ob.findall(release_time[0])

        imgs = self.hxs.select("//div[@class='tbrig']")[0].select('./p/img/@src').extract()
        img_all = []
        for img in imgs:
            if".gif" in img:
                continue
            if".GIF" in img:
                continue
            else: 
                img_all.append(self.getRealURI(img))
        item['image_urls'] = img_all
        
        item['title'] = self.title = title[0]
        item['content'] = self.content = all_content
        item['release_time'] = release_time[0]
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time[0],u'%Y-%m-%d %H:%M'))
        item['source'] = u"39健康问答"
        item['author'] = tz_author[0]        
        item['pic_url'] = ''
        
        self.title = item['title']
        self.content = item['content']
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False