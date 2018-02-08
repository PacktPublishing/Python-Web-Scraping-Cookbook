from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy import Request
import urllib.parse

class LinkReferenceCount:
    def __init__(self, link):
        self.link = link
        self.count = 0


class PageToPageMap:
    def __init__(self, link, child_link, depth): #, parent):
        self.link = link
        self.child_link = child_link
        self.title = self.get_page_title(self.link)
        self.child_title = self.get_page_title(self.child_link)
        self.depth = depth

    def get_page_title(self, link):
        parts = link.split("/")
        last = parts[len(parts)-1]
        label = urllib.parse.unquote(last)
        return label


class WikipediaSpider(Spider):
    name = "wikipedia"
    start_urls = [ "https://en.wikipedia.org/wiki/Python_(programming_language)" ]

    page_map = {}
    linked_pages = []
    max_items_per_page = 5
    max_crawl_depth = 1

    def parse(self, response):
        print("parsing: " + response.url)

        links = response.xpath("//*/a[starts-with(@href, '/wiki/')]/@href")

        depth = 0
        if "parent" in response.meta:
            parent = response.meta["parent"]
            depth = parent.depth + 1

        if depth >= self.max_crawl_depth: return

        link_counter = {}

        for l in links:
            link = l.root
            if ":" not in link and "International" not in link and link != self.start_urls[0]:
                if link not in link_counter:
                    link_counter[link] = LinkReferenceCount(link)
                link_counter[link].count += 1

        references = list(link_counter.values())
        s = sorted(references, key=lambda x: x.count, reverse=True)
        top = s[:self.max_items_per_page]

        for child_page in top:
            pm = PageToPageMap(response.url, "https://en.wikipedia.org" + child_page.link, depth)
            self.linked_pages.append(pm)

        # go crawl those found pages
        for item in top:
            new_request = Request("https://en.wikipedia.org" + item.link,
                                  callback=self.parse, meta={ "parent": pm })
            yield new_request
