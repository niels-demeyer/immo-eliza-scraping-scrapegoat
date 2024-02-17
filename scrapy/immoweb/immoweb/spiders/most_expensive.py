import scrapy


class MostExpensiveSpider(scrapy.Spider):
    name = "most_expensive"
    allowed_domains = ["www.immoweb.be"]
    start_urls = ["https://www.immoweb.be/en/"]

    def parse(self, response):
        pass
