import scrapy


class IgbospiderSpider(scrapy.Spider):
    name = 'igbospider'
    allowed_domains = ['myigboname.com']
    start_urls = ['https://www.myigboname.com/start-with/a']

    def parse(self, response):
        names = response.css('.content a')
        
        for name in names:
            yield{
                'name' : name.css(' a::text').get(),
                'url' : 'https://www.myigboname.com/{0}'.format(name.css('a::attr(href)').get())
            }
