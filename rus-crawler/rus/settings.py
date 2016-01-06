# -*- coding: utf-8 -*-

# see also https://github.com/knockrentals/scrapy-elasticsearch

BOT_NAME = 'rus'

SPIDER_MODULES = ['rus.spiders']
NEWSPIDER_MODULE = 'rus.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'FIXME'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY=1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'rus.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'rus.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
EXTENSIONS = {
#    'scrapy.extensions.closespider.CloseSpider': 500,
}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline',
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED=True
HTTPCACHE_EXPIRATION_SECS=0
HTTPCACHE_DIR='httpcache'
HTTPCACHE_IGNORE_HTTP_CODES=[]
HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPCACHE_GZIP=True

from scrapy import log
import os

ELASTICSEARCH_SERVER = 'http://{}'.format(os.environ['ES_PORT_9200_TCP_ADDR'])
ELASTICSEARCH_PORT = int(os.environ['ES_PORT_9200_TCP_PORT'])
ELASTICSEARCH_USERNAME = os.environ.get('ES_USERNAME','')
ELASTICSEARCH_PASSWORD = os.environ.get('ES_PASSWORD','')
ELASTICSEARCH_INDEX = os.environ.get('ES_INDEX','rus')
ELASTICSEARCH_TYPE = 'items'
ELASTICSEARCH_UNIQ_KEY = 'url'  # Custom uniqe key like 'student_id'
ELASTICSEARCH_LOG_LEVEL= log.DEBUG

# CLOSESPIDER_ERRORCOUNT = 1

LOG_LEVEL = 'INFO'
DOWNLOAD_WARNSIZE = ( 1024 ** 2 ) * 100


# This code changes the `url` property to be `not_analyzed` which
# allows later prefix search operations to work properly.
# It would be nice if scrapy elastic search had a mechanism for setting this.

from elasticsearch import Elasticsearch

es = Elasticsearch('{}:{}'.format(ELASTICSEARCH_SERVER, ELASTICSEARCH_PORT))
if not es.indices.exists(ELASTICSEARCH_INDEX):
    es.indices.create(index=ELASTICSEARCH_INDEX,
                      body="""
{
    "mappings": {
	"items" : {
	    "properties" : {
		"url" : {
		    "type": "string",
		    "index": "not_analyzed"
		      },
		"contenttype" : {
		    "type": "string",
		    "index": "not_analyzed"
		}
	    }
	}
    }
}
                      """,
                      )
