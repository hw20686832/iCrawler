#coding: utf-8
import redis
from scrapy.conf import settings

rconf = settings.get('REDIS_CONF')

cs = redis.Redis(host = rconf['HOST'], 
                 port = rconf['PORT'],
                 password = rconf['PASSWORD'],
                 db = rconf['DB'])
