from typing import Iterable
import scrapy


class MostExpensiveSpider(scrapy.Spider):
    name = "most_expensive"
    allowed_domains = ["www.immoweb.be"]
    start_urls = ["https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=1&orderBy=most_expensive"]
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        title = response.css('title::text').get()
        yield {
            'title': title,
        }
