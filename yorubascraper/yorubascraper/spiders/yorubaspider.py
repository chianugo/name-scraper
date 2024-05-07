import scrapy


class YorubaspiderSpider(scrapy.Spider):
    name = "yorubaspider"
    allowed_domains = ["yorubaname.com"]
    start_urls = ["https://www.yorubaname.com/alphabets/a"]

    def parse(self, response):
        names = response.css('ul a.name')
        
        for name in names:
            pass
