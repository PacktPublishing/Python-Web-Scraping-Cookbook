import scrapy
from scrapy.crawler import CrawlerProcess

class Spider(scrapy.Spider):
    name = 'spider'
    start_urls = ['https://blog.scrapinghub.com']

    def parse(self, response):
        print("Parsing: ", response)

        for next_page in response.css('div.prev-post > a'):
            yield response.follow(next_page, self.parse)

    def close(spider, reason):
        start_time = spider.crawler.stats.get_value('start_time')
        finish_time = spider.crawler.stats.get_value('finish_time')
        print("Total run time: ", finish_time-start_time)

if __name__ == "__main__":
    process = CrawlerProcess({
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOADER_MIDDLEWARES':
            {
                "scrapy.downloadermiddlewares.retry.RetryMiddleware": 500
            },
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 3
    })
    process.crawl(Spider)
    process.start()
