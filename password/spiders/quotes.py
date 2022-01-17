import scrapy
import lxml.html as html
from scrapy import FormRequest
from ..items import QuoteTutorialItem


TOKEN = 'body//input[@name="csrf_token"]/@value'

class QuotesScraper(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/login'
    ]


    def parse(self, response):
        token = response.xpath(TOKEN).get()
        return FormRequest.from_response(response, 
        formdata={
            'csrf_token': token,
            'username': 'juan_perez',
            'password': '13212'
        },
        callback=self.start_scraping
        )

    def start_scraping(self, response):
        items = QuoteTutorialItem()

        all_div_quotes = response.xpath('//div[@class="quote"]').getall()


        for quotes in all_div_quotes:
            html_quotes = html.fromstring(quotes)
            title = html_quotes.xpath('//span[@class="text"]/text()')
            author = html_quotes.xpath('//small[@class="author"]/text()')
            tag = html_quotes.xpath('//div[@class="tags"]/a[@class="tag"]/text()')

            items['title'] = title
            items['author'] = author
            items['tag'] = tag

            yield items

