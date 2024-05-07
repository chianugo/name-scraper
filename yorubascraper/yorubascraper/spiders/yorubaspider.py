from typing import Iterable
from scrapy.exporters import CsvItemExporter
import scrapy


class YorubaspiderSpider(scrapy.Spider):
    name = "yorubaspider"
    allowed_domains = ["yorubaname.com"]
    start_urls = ["https://www.yorubaname.com/alphabets/a"]

    items = []
    def parse(self, response):
        names = response.css('a.name')
        
        for name in names:
            meaning_page_url = 'https://www.yorubaname.com{0}'.format(name.attrib['href'])
            yield scrapy.Request(meaning_page_url, callback=self.parseMeaning)
            
    def parseMeaning(self, response):
        print('item 2')
        glosses = []
        gloss_elements = response.css('h4:contains("Gloss") + strong')
        for element in gloss_elements:
            term = element.css('strong::text').get()
            description = element.xpath('following-sibling::span[1]/text()').get()
            glosses.append({term: description})

        item = {
            'name' : response.css('#name-entry::text').get().strip(),
            'transcription' : response.css('h4:contains("Morphology") + p::text').get(default='-').strip(),
            'meaning' : response.css('h4:contains("Meaning of") +p::text').get(default='unknown').strip(),
            'extended meaning': response.css('h4:contains("Extended Meaning") + p::text').get(default='unknown').strip(),
            'gloss': glosses,
            'language' :'yoruba' 
        }

        self.items.append(item)
        yield item
        
    # def closed(self, reason):
    #     sorted_items = sorted(self.items, key=lambda x: x['name'])  # Sort items alphabetically by 'name'
    #     exporter = CsvItemExporter(open("yoruba.csv", "wb"))  # Open CSV file for writing
    #     exporter.start_exporting()
    #     for item in sorted_items:
    #         exporter.export_item(item)
    #     exporter.finish_exporting()

    def spider_closed(self, spider):
        sorted_items = sorted(self.items, key=lambda x: x['name'])  # Sort items alphabetically by 'name'
        with open("yoruba.csv", "w", newline='', encoding='utf-8') as csvfile:  # Open CSV file for writing
            exporter = CsvItemExporter(csvfile)
            exporter.start_exporting()
            for item in sorted_items:
                exporter.export_item(item)
            exporter.finish_exporting()