import scrapy
from scrapy.crawler import CrawlerProcess

class Spider(scrapy.Spider):
    name = 'spider'
    start_urls = [
#        'http://www.amazon.com/',
#        'http://www.amazon.com/gp/dmusic/',
#        'http://www.amazon.com/gp/dmusic/promotions/PrimeMusic/',
        'https://www.amazon.com/gp/registry/wishlist/'
    ]

    def parse(self, response):
        print("Parsing: ", response)

if __name__ == "__main__":
    process = CrawlerProcess({
        'DOWNLOAD_DELAY': 5,
        'RANDOMIZED_DOWNLOAD_DELAY': False,
        'LOG_LEVEL': 'DEBUG'
    })
    process.crawl(Spider)
    process.start()
