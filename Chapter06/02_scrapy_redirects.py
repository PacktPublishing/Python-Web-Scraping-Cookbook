import scrapy
from scrapy.crawler import CrawlerProcess

class Spider(scrapy.spiders.SitemapSpider):
    name = 'spider'
    sitemap_urls = ['https://www.nasa.gov/sitemap.xml']

    def parse(self, response):
        print("Parsing: ", response)
        print (response.request.meta.get('redirect_urls'))

if __name__ == "__main__":
    process = CrawlerProcess({
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOADER_MIDDLEWARES':
            {
                "scrapy.downloadermiddlewares.redirect.RedirectMiddleware": 500
            },
        'REDIRECT_ENABLED': True,
        'REDIRECT_MAX_TIMES': 2
    })
    process.crawl(Spider)
    process.start()
