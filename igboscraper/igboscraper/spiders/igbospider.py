import scrapy


class IgbospiderSpider(scrapy.Spider):
    name = 'igbospider'
    allowed_domains = ['myigboname.com']
    start_urls = ['http://myigboname.com/']

    def parse(self, response):
        pass
