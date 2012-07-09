# Scrapy settings for youwa project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import time

BOT_NAME = 'yowa'
BOT_VERSION = '1.5'

#LOG_LEVEL = 'INFO'
#ROBOTSTXT_OBEY = True
DOWNLOAD_TIMEOUT = 180

SPIDER_MODULES = ['yowa.spiders']
TEMPLATE_MODULES = 'yowa.templates'
NEWSPIDER_MODULE = 'yowa.spiders'
#DEFAULT_ITEM_CLASS = 'yowa.items.ContentItem'
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; .NET4.0C; .NET4.0E)'

IMAGES_INTERVAL = time.strftime('%Y-%m-%d')
IMAGES_STORE = '/share/youwa/spider/images/%s/' % IMAGES_INTERVAL
IMAGES_THUMBS = {'small': (96, 96),
                 'big': (294, 294)}

ITEM_PIPELINES = ['yowa.pipelines.YowaPipeline', 
                  'yowa.pipelines.DaemonPipeline']

#EXTENSIONS = {'yowa.extensions.sqla.Sqla_connection': 500, }

REDIS_CONF = {'HOST': '192.168.1.2',
              'PORT': 6379,
              'PASSWORD': 'ky2379ck$', 
              'DB': 1}

DB_CONF = {'DIALECT': 'oracle+cx_oracle',
           'SERVICE_NAME': 'TEST',
           'USERNAME': 'ngic1',
           'PASSWORD': 'ngic1'}

DUPEFILTER_CLASS = 'yowa.middlewares.dupeFilter.RedisDupeFilter'

WEBKIT_DOWNLOADER = ['ly_xw', 'all_bk']
DOWNLOADER_MIDDLEWARES = {'yowa.middlewares.webkitDownloader.WebkitDownloader': 543, }
