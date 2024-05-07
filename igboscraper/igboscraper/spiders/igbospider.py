from typing import Iterable
from scrapy.exporters import CsvItemExporter
import scrapy


class IgbospiderSpider(scrapy.Spider):
    name = 'igbospider'
    allowed_domains = ['myigboname.com']
    start_urls = ['https://www.myigboname.com/start-with/a',
                  'https://www.myigboname.com/start-with/b',
                  'https://www.myigboname.com/start-with/c',
                  'https://www.myigboname.com/start-with/d',
                  'https://www.myigboname.com/start-with/e',
                  'https://www.myigboname.com/start-with/f',
                  'https://www.myigboname.com/start-with/g',
                  'https://www.myigboname.com/start-with/i',
                  'https://www.myigboname.com/start-with/j',
                  'https://www.myigboname.com/start-with/k',
                  'https://www.myigboname.com/start-with/l',
                  'https://www.myigboname.com/start-with/m',
                  'https://www.myigboname.com/start-with/n',
                  'https://www.myigboname.com/start-with/o',
                  'https://www.myigboname.com/start-with/r',
                  'https://www.myigboname.com/start-with/s',
                  'https://www.myigboname.com/start-with/t',
                  'https://www.myigboname.com/start-with/u',
                  'https://www.myigboname.com/start-with/w',
                  'https://www.myigboname.com/start-with/z',]
    items =[]

    def parse(self, response):
        names = response.css('.content a')
        
        for name in names:
            meaning_page_url =  'https://www.myigboname.com{0}'.format(name.css('a::attr(href)').get())
            yield scrapy.Request(meaning_page_url, callback=self.parseMeaning)

    def parseMeaning(self, response):
        
        item = {
            'name' : response.css('h1::text').get().strip(),
            'transcription': response.css('.very p::text').get(default='-').strip(),
            'meaning' : response.css('div.very.padded h1 + p + p + p strong::text').get(default='unknown').strip(),
            'gender': response.css('.very:last-child strong::text').get(default='-'),
            'language': 'igbo'
            
        }
        self.items.append(item)
        yield item
        
    def closed(self, reason):
        sorted_items = sorted(self.items, key=lambda x: x['name'])  # Sort items alphabetically by 'name'
        exporter = CsvItemExporter(open("igbo.csv", "wb"))  # Open CSV file for writing
        exporter.start_exporting()
        for item in sorted_items:
            exporter.export_item(item)
        exporter.finish_exporting()