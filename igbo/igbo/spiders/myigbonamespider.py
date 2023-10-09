import scrapy


class MyigbonamespiderSpider(scrapy.Spider):
    name = 'myigbonamespider'
    allowed_domains = ['myigboname.com']
    start_urls = ['http://myigboname.com/']

    def parse(self, response):
        pass
