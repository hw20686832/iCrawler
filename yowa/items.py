# coding: utf-8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
from scrapy.item import Item, Field

class ContentItem(Item):
    father_url_number = Field()
    title = Field()
    content = Field()
    source = Field()
    author = Field()
    climb_time = Field()
    release_switch_time = Field()
    release_time = Field()
    child_url = Field()
    pic_url = Field()
    price = Field()
    city = Field()
    merchant = Field()
    deadline = Field()
    sum_mark = Field()
    child_mark = Field()
    images = Field()
    image_urls = Field()
    shop = Field()
    validity = Field()
    code = Field()
    today_date = Field()
    opening = Field()
    closing = Field()
    type = Field()


    def withdict(self, ):
        return dict(father_url_number = self.get('father_url_number'), 
                    title = self.get('title'), 
                    content = self.get('content'), 
                    source = self.get('source'), 
                    author = self.get('author'), 
                    climb_time = self.get('climb_time'), 
                    release_switch_time = self.get('release_switch_time'), 
                    release_time = self.get('release_time'), 
                    child_url = self.get('child_url'), 
                    image_urls = self.get('image_urls'), 
                    pic_url = self.get('pic_url'), 
                    price = self.get('price'),
                    merchant = self.get('merchant'), 
                    deadline = self.get('deadline'), 
                    city = self.get('city'), 
                    sum_mark = self.get('sum_mark'), 
                    child_mark = self.get('child_mark'),
                    code = self.get('code'),
                    today_date = self.get('today_date'),
                    opening = self.get('opening'),
                    closing = self.get('closing'),
                    type = self.get('type'))

    def __str__(self):
        if self.get('code'):
            #print self.get('code')
            return "ContentItem(code = '%(code)s', child_url = '%(child_url)s')" % self
        else:
            return "ContentItem(child_url = '%(child_url)s', title = '%(title)s')" % self
