import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector

class Spider(scrapy.spiders.SitemapSpider):
    name = 'spider'
    sitemap_urls = ['https://www.nasa.gov/sitemap.xml']
    allowed_domains=['nasa.gov']

    def parse(self, response):
        print("Parsing: ", response)
        sel = Selector(response)
        items = sel.xpath("//*/a").extract()
        for i in items:
            print(i)

if __name__ == "__main__":
    process = CrawlerProcess({
        'LOG_LEVEL': 'DEBUG'
    })
    process.crawl(Spider)
    process.start()
