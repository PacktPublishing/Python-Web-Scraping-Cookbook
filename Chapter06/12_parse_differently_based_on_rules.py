import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.crawler import CrawlerProcess

class MySpider(CrawlSpider):
    # The name of the spider
    name = "datablogger"

    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ["xkcd.com"]

    # The URLs to start with
    start_urls = ["https://xkcd.com/"]

    # This spider has one rule: extract all (unique and canonicalized) links, follow them and parse them using the parse_items method
    rules = [
        Rule(
            LinkExtractor(
                allow=(),
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]

    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    # Method for parsing items
    def parse_items(self, response):
        print(response)


if __name__ == "__main__":
    process = CrawlerProcess({
        'LOG_LEVEL': 'INFO',
        'CLOSESPIDER_PAGECOUNT': 50
    })
    process.crawl(MySpider)
    process.start()