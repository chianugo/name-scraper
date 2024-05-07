from typing import Iterable
from scrapy.exporters import CsvItemExporter
import scrapy


class YorubaspiderSpider(scrapy.Spider):
    name = "yorubaspider"
    allowed_domains = ["yorubaname.com"]
    start_urls = ["https://www.yorubaname.com/alphabets/a",
                  "https://www.yorubaname.com/alphabets/b",
                  "https://www.yorubaname.com/alphabets/d",
                  "https://www.yorubaname.com/alphabets/e",
                  "https://www.yorubaname.com/alphabets/g",
                  "https://www.yorubaname.com/alphabets/gb",
                  "https://www.yorubaname.com/alphabets/h",
                  "https://www.yorubaname.com/alphabets/i",
                  "https://www.yorubaname.com/alphabets/j",
                  "https://www.yorubaname.com/alphabets/k",
                  "https://www.yorubaname.com/alphabets/l",
                  "https://www.yorubaname.com/alphabets/m",
                  "https://www.yorubaname.com/alphabets/n",
                  "https://www.yorubaname.com/alphabets/ọ",
                  "https://www.yorubaname.com/alphabets/o",
                  "https://www.yorubaname.com/alphabets/p",
                  "https://www.yorubaname.com/alphabets/r",
                  "https://www.yorubaname.com/alphabets/s",
                  "https://www.yorubaname.com/alphabets/ṣ",
                  "https://www.yorubaname.com/alphabets/t",
                  "https://www.yorubaname.com/alphabets/u",
                  "https://www.yorubaname.com/alphabets/w",
                  "https://www.yorubaname.com/alphabets/y"]

    items = []
    def parse(self, response):
        names = response.css('a.name')
        
        for name in names:
            meaning_page_url = 'https://www.yorubaname.com{0}'.format(name.attrib['href'])
            yield scrapy.Request(meaning_page_url, callback=self.parseMeaning)
            
    def parseMeaning(self, response):
        glosses = []
        gloss_elements = response.css('h4:contains("Gloss") + strong')
        for element in gloss_elements:
            term = element.css('strong::text').get()
            description = element.xpath('following-sibling::span[1]/text()').get()
            glosses.append({term: description})
            
        meaning_text = response.xpath('//p[@class="intonation"]/text()').get()
        if meaning_text:
            meaning_text = meaning_text.strip()
            meaning_text = ' '.join(meaning_text.split()) 

        item = {
            'name' : response.css('#name-entry::text').get().strip(),
            'transcription' : response.css('h4:contains("Morphology") + p::text').get(default='-').strip(),
            'meaning' : meaning_text if meaning_text else 'unknown',
            'extended meaning': response.css('h4:contains("Extended Meaning") + p::text').get(default='unknown').strip(),
            'gloss': glosses,
            'language' :'yoruba' 
        }

        self.items.append(item)
        yield item
        
    def closed(self, reason):
        sorted_items = sorted(self.items, key=lambda x: x['name'])  # Sort items alphabetically by 'name'
        exporter = CsvItemExporter(open("yoruba.csv", "wb"))  # Open CSV file for writing
        exporter.start_exporting()
        for item in sorted_items:
            exporter.export_item(item)
        exporter.finish_exporting()