from typing import Iterable
import scrapy
import logging


class MostExpensiveSpider(scrapy.Spider):
    name = "most_expensive"
    allowed_domains = ["www.immoweb.be"]
    start_urls = ["https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=1&orderBy=most_expensive"]
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        for h2 in response.css('h2'):
            link = h2.css('a')
            if link:
                href = link.css('::attr(href)').get()
                title = link.css('::text').get()
                if title is not None:
                    title = title.strip()
                yield {
                    'href': href,
                    'title': title,
                }
            else:
                logging.info(f"No 'a' tag found in this 'h2' element")