import scrapy


# class MyigbonamespiderSpider(scrapy.Spider):
#     name = 'myigbonamespider'
#     allowed_domains = ['myigboname.com']
#     start_urls = ['http://myigboname.com/']

#     def parse(self, response):
#         names = response.css('.flexi .item .content')

#         for name in names:
#             start_with_url = name.css('a::attr(href)').get()

#             if start_with_url is not None:
#                 letter_url = 'https://www.myigboname.com' + start_with_url
#                 yield response.follow(letter_url, callback=self.parse)

#             begin_with_letter = response.css('.ui .item .content a')
#             for name in begin_with_letter:
#                 name_url = name.css('a::attr(href)').get()

#                 if name_url is not None:
#                     yield response.follow(name_url, callback=self.parse_name_page)

#     def parse_letter_page(self, response):
#         pass

#     def parse_name_page(self, response):

#         yield {
#             "name": response.css('.very h1::text').get(),
#             "transcription": response.xpath('/html/body/div[2]/div/div/div[2]/div/p[1]/text()').get(),
#             "language": "Igbo",
#             "gender": response.xpath('/html/body/div[2]/div/div/div[2]/div/p[2]/strong/text()').get().strip(),
#             'meaning': response.xpath('/html/body/div[2]/div/div/div[2]/div/p[3]/strong/text()').get().strip(),
#         }


class MyigbonamespiderSpider(scrapy.Spider):
    name = 'myigbonamespider'
    allowed_domains = ['myigboname.com']
    start_urls = ['http://myigboname.com/']

    def parse(self, response):
        # names = response.css('.flexi .item .content')
        names = [url.strip() for url in response.css(
            '.flexi .item .content a::attr(href)')]
        # names = [url.strip() for url in response.css(
        #     '.flexi .item .content a::attr(href)').getall()]

        for name in names:
            # start_with_url = name.css('a::attr(href)').get()
            start_with_url = name

            if start_with_url is not None:
                letter_url = 'https://www.myigboname.com' + start_with_url
                print('********************************')
                print(letter_url)
                name_response = response.follow(
                    letter_url, callback=self.parse_letter_page)
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>.')
                print(name_response)

                begin_with_letter = name_response.css('.ui .item .content a')
                for name in begin_with_letter:
                    name_url = name.css('a::attr(href)').get()
                    print(
                        '----------------------------------------------------------------')
                    print(name_url)

                    if name_url is not None:
                        yield response.follow(name_url, callback=self.parse_name_page)

    def parse_letter_page(self, response):
        print('++++++++++++++++++++++++++++++++++++')
        self.logger.info('visited %s', response.url)

    def parse_name_page(self, response):

        yield {
            "name": response.css('.very h1::text').get(),
            "transcription": response.xpath('/html/body/div[2]/div/div/div[2]/div/p[1]/text()').get(),
            "language": "Igbo",
            "gender": response.xpath('/html/body/div[2]/div/div/div[2]/div/p[2]/strong/text()').get().strip(),
            'meaning': response.xpath('/html/body/div[2]/div/div/div[2]/div/p[3]/strong/text()').get().strip(),
        }
