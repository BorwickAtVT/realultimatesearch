import re
import tempfile
from urlparse import urlparse

import textract

from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from rus.items import RusItem

WHITESPACE_RE = re.compile('\s{2,}')


def excerpt_from_text(all_text):
    return all_text[:200]


class RusSpider(CrawlSpider):
    name = "rus"
    allowed_domains = [
        'FIXME',
        'FIXME',
    ]
    start_urls = [
        'FIXME',
        'FIXME',
    ]
    url_patterns_to_block = [
        'FIXME',
    ]
    
    rules = (
        Rule (LinkExtractor(allow=re.compile('\.csv$'),
                            deny_extensions=()),
              callback='parse_csv',
        ),
        Rule (LinkExtractor(allow=re.compile('\.doc$'),
                            deny_extensions=()),
              callback='parse_doc',
        ),
        Rule (LinkExtractor(allow=re.compile('\.docx$'),
                            deny_extensions=()),
              callback='parse_docx',
        ),
        Rule (LinkExtractor(allow=re.compile('\.eml$'),
                            deny_extensions=()),
              callback='parse_eml',
        ),
        Rule (LinkExtractor(allow=re.compile('\.msg$'),
                            deny_extensions=()),
              callback='parse_msg',
        ),
        Rule (LinkExtractor(allow=re.compile('\.pdf$'),
                            deny_extensions=()),
              callback='parse_pdf',
        ),
        Rule (LinkExtractor(allow=re.compile('\.pptx$'),
                            deny_extensions=()),
              callback='parse_pptx',
        ),
        Rule (LinkExtractor(allow=re.compile('\.ps$'),
                            deny_extensions=()),
              callback='parse_ps',
        ),
        Rule (LinkExtractor(allow=re.compile('\.rtf$'),
                            deny_extensions=()),
              callback='parse_rtf',
        ),
        Rule (LinkExtractor(allow=re.compile('\.txt$'),
                            deny_extensions=()),
              callback='parse_txt',
        ),
        Rule (LinkExtractor(allow=re.compile('\.xls$'),
                            deny_extensions=()),
              callback='parse_xls',
        ),
        Rule (LinkExtractor(allow=re.compile('\.xlsx$'),
                            deny_extensions=()),
              callback='parse_xlsx',
        ),

        Rule (LinkExtractor(),
              callback='parse_item',
              process_links='process_links',
              follow=True),
    )

    def parse_item(self, response):
        item = RusItem()
        item['url'] = response.url
        item['netloc'] = urlparse(response.url).netloc
        item['contenttype'] = response.headers['Content-type']
        item['title'] = u''.join(response.xpath('//title/text()').extract())
        all_text = u' '.join(response.xpath('//body//*[not(self::script)]//text()').extract())
        all_text = WHITESPACE_RE.sub(' ', all_text)
        item['fulltext'] = all_text
        item['excerpt'] = excerpt_from_text(all_text)
        return item

    # from
    # http://stackoverflow.com/questions/13508484/linkextraction-for-scrapy-global-deny
    def process_links(self, links):
        return [link for link in links if self.valid_link(link)]

    def valid_link(self, link):
        # if the link is in any of the url_patterns_to_block:
        if any([pattern.search(link.url) for pattern in self.url_patterns_to_block]):
            return False
        else:
            return True
        
    def parse_textract(self, response, extension):
        """
        This method uses the `textract` module to pull text out.

        It does not populate the title, but it populates the text.


        """
        with tempfile.NamedTemporaryFile(suffix=extension) as tmpfile:
            tmpfile.write(response.body)
            tmpfile.flush()
            all_text = textract.process(tmpfile.name)
            
            item = RusItem()
            item['url'] = response.url
            item['netloc'] = urlparse(response.url).netloc

            item['contenttype'] = response.headers['Content-type']
            item['fulltext'] = all_text
            item['excerpt'] = excerpt_from_text(all_text)
            return item

    def parse_csv(self, response):
        return self.parse_textract(response, extension='.csv')

    def parse_doc(self, response):
        return self.parse_textract(response, extension='.doc')

    def parse_docx(self, response):
        return self.parse_textract(response, extension='.docx')

    def parse_eml(self, response):
        return self.parse_textract(response, extension='.eml')

    def parse_msg(self, response):
        return self.parse_textract(response, extension='.msg')

    def parse_pdf(self, response):
        return self.parse_textract(response, extension='.pdf')

    def parse_pptx(self, response):
        return self.parse_textract(response, extension='.pptx')

    def parse_ps(self, response):
        return self.parse_textract(response, extension='.ps')

    def parse_rtf(self, response):
        return self.parse_textract(response, extension='.rtf')

    def parse_txt(self, response):
        return self.parse_textract(response, extension='.txt')

    def parse_xls(self, response):
        return self.parse_textract(response, extension='.xls')

    def parse_xlsx(self, response):
        return self.parse_textract(response, extension='.xlsx')
