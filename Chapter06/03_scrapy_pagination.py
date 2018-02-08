from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class PaginatedSearchResultsSpider(CrawlSpider):
    name = "paginationscraper"
    start_urls = [
        "http://localhost:5001/pagination/page1.html"
    ]
    rules = (
        # Extract links for next pages
        Rule(LinkExtractor(allow=(),
                           restrict_xpaths=("//*/a[@class='next']")),
                           callback='parse_result_page', follow=True),
    )
    all_items = []

    def parse_start_url(self, response):
        return self.parse_result_page(response)

    def parse_result_page(self, response):
        data_items = response.xpath("//*/div[@class='data']/h1/text()")
        for data_item in data_items:
            self.all_items.append(data_item.root)

    def closed(self, reason):
        for i in self.all_items:
            print(i)

if __name__ == "__main__":
    process = CrawlerProcess({
        'LOG_LEVEL': 'DEBUG',
        'CLOSESPIDER_PAGECOUNT': 10
    })
    process.crawl(PaginatedSearchResultsSpider)
    process.start()
