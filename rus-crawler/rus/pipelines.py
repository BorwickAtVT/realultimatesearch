# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import os

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

from scrapy.exceptions import DropItem


class RusPipeline(object):
    def process_item(self, item, spider):
        return item


class BareURLChecksumPipeline(object):
    def __init__(self):
        self.es = Elasticsearch(os.environ['ES_PORT_9200_TCP_ADDR'],
                                port=os.environ['ES_PORT_9200_TCP_PORT'])

    def already_seen(self, checksum, bare_url):
        s = Search(using=self.es).query("term",
                                        checksum=checksum
                                        ).query("term",
                                                bare_url=bare_url)
        resp = s.execute()
        if resp.hits.total > 0:
            return True
        else:
            return False


    def process_item(self, item, spider):
        fulltext = item['fulltext']
        try:
            fulltext.decode('utf-8')
        except UnicodeError:
            fulltext = fulltext.encode('utf-8')
        checksum = hashlib.sha256(fulltext).hexdigest()
        bare_url = item.get_bare_url()
        item['checksum'] = checksum
        item['bare_url'] = bare_url

        if self.already_seen(checksum, bare_url):
            raise DropItem("Duplicate item found: %s" % item)
        else:
            return item
