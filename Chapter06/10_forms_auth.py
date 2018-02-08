import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector

class Spider(scrapy.Spider):
    name = 'spider'
    start_urls = ['http://localhost:5001/home/secured']

    login_user = 'darkhelmet'
    login_pass = 'vespa'

    @property
    def crawled_urls(self):
        return self._crawled_urls

    def __init__(self, stats):
        self.stats = stats
        self._crawled_urls = []

    def parse(self, response):
        print("Parsing: ", response)

        count_of_password_fields = int(float(response.xpath("count(//*/input[@type='password' and @id='Password'])").extract()[0]))
        if count_of_password_fields > 0:
            print("Got a password page")
            return scrapy.FormRequest.from_response(
                response,
                formdata={'Username': self.login_user, 'Password': self.login_pass},
                callback=self.after_login)
        else:
            pass

    def after_login(self, response):
        if "This page is secured" in str(response.body):
            print("You have logged in ok!")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(stats=crawler.stats)

if __name__ == "__main__":
    process = CrawlerProcess({
        'LOG_LEVEL': 'DEBUG',
#        'DEPTH_LIMIT': 10,
#        'DEPTH_STATS': True,
#        'CLOSESPIDER_PAGECOUNT': 30
    })

    process.crawl(Spider)
    spider = next(iter(process.crawlers)).spider
    process.start()
    stats = spider.stats
    print(stats)
    print(spider.crawled_urls)