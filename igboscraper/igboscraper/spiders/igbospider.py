import scrapy


class IgbospiderSpider(scrapy.Spider):
    name = 'igbospider'
    allowed_domains = ['myigboname.com']
    start_urls = ['http://myigboname.com/start-with/a']

    def parse(self, response):
        names = response.css('.content a::text').getall()
        
        for name in names:
            yield{
                'name' : name.css('.content a::text').get(),
                'url' : name.css('.content a::attr(href)').get()
            }
