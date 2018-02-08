import json
import scrapy
from scrapy.crawler import CrawlerProcess

class Spider(scrapy.Spider):
    name = 'spidyquotes'
    quotes_base_url = 'http://spidyquotes.herokuapp.com/api/quotes'
    start_urls = [quotes_base_url]
    download_delay = 1.5

    def parse(self, response):
        print(response)
        data = json.loads(response.body)
        for item in data.get('quotes', []):
            yield {
                'text': item.get('text'),
                'author': item.get('author', {}).get('name'),
                'tags': item.get('tags'),
            }
        if data['has_next']:
            next_page = data['page'] + 1
            yield scrapy.Request(self.quotes_base_url + "?page=%s" % next_page)

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(Spider)
    process.start()