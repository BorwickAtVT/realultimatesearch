# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import re
import urlparse

import scrapy


NONWORD_RE = re.compile(r'\W+')


class RusItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    contenttype = scrapy.Field()
    excerpt = scrapy.Field()
    url = scrapy.Field()
    fulltext = scrapy.Field()
    bare_url = scrapy.Field()
    checksum = scrapy.Field()

    def get_bare_url(self):
        """
        OK, so the thinking behind this

        1. Sometimes there are checksum collisions

        2. There are sometimes many ways to access the same content
        e.g. http:, https:

        So, this tries to give a balance of the two. bare_url +
        checksum should be a pretty good unique identifier.

        The rules for bare_url are pretty, well, bare. The returned
        URL should be the netloc
        """
        url_parts = urlparse.urlparse(self['url'])
        url_path = url_parts.path
        host = url_parts.netloc.lower()
        bare_url_path = NONWORD_RE.sub('-', url_path).lower()
        return '{}/{}'.format(host, bare_url_path)
