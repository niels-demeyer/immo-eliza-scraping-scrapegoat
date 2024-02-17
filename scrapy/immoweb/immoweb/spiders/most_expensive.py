from typing import Iterable
import scrapy
import logging


class MostExpensiveSpider(scrapy.Spider):
    name = "most_expensive"
    allowed_domains = ["www.immoweb.be"]
    start_urls = ["https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=1&orderBy=most_expensive"]
    
    def start_requests(self):
        base_url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={}&orderBy=most_expensive"
        for i in range(1, 10):  # Change 101 to the number of pages you want to scrape + 1
            yield scrapy.Request(url=base_url.format(i), callback=self.parse)
    
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