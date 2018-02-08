import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector

class Spider(scrapy.Spider):
    name = 'spider'
    start_urls = ['http://localhost:5001/CrawlDepth0-1.html']

    @property
    def parsed_urls(self):
        return self._parsed_urls
    @property
    def requested_urls(self):
        return self._requested_urls

    def __init__(self, stats):
        self.stats = stats
        self._parsed_urls = []
        self._requested_urls = []


    def parse(self, response):
        self._parsed_urls.append(response.url)
        print("Parsing: ", response)

        sel = Selector(response)
        urls = sel.xpath("//*/a/@href").extract()
        for url in urls:
            full_url = response.urljoin(url)
            print("Requesting crawl of: ", full_url)
            self._requested_urls.append(full_url)
            yield scrapy.Request(response.urljoin(url), callback=self.parse)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(stats=crawler.stats)

if __name__ == "__main__":
    process = CrawlerProcess({
        'LOG_LEVEL': 'CRITICAL',
        'DEPTH_LIMIT': 2,
        'DEPT_STATS': True
    })

    process.crawl(Spider)
    spider = next(iter(process.crawlers)).spider
    process.start()
    stats = spider.stats
    print(stats)
    print("Crawled: ", spider.parsed_urls)
    print("Requested: ", spider.requested_urls)