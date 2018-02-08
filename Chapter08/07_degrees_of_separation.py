from wikipedia.spiders import WikipediaSpider
from scrapy.crawler import CrawlerProcess
import networkx as nx
import matplotlib.pyplot as plt
import urllib.parse

if __name__ == "__main__":
    crawl_depth = 2
    process = CrawlerProcess({
        'LOG_LEVEL': 'ERROR',
        'DEPTH_LIMIT': crawl_depth
    })
    process.crawl(WikipediaSpider)
    spider = next(iter(process.crawlers)).spider
    spider.max_items_per_page = 5
    spider.max_crawl_depth = crawl_depth
    process.start()

    for pm in spider.linked_pages:
        print(pm.depth, pm.link, pm.child_link)
    print("-"*80)

    g = nx.Graph()

    nodes = {}
    edges = {}


    for pm in spider.linked_pages:
        if pm.title not in nodes:
            nodes[pm.title] = pm
            g.add_node(pm.title)

        if pm.child_title not in nodes:
            g.add_node(pm.child_title)

        link_key = pm.title + " ==> " + pm.child_title
        if link_key not in edges:
            edges[link_key] = link_key
            g.add_edge(pm.title, pm.child_title)

    labels = { node: node for node in g.nodes() }

    path = nx.astar_path(g, "Python_(programming_language)", "Dennis_Ritchie")

    # report
    degrees_of_separation = int((len(path) - 1) / 2)
    print("Degrees of separation: {}".format(degrees_of_separation))
    for i in range(0, len(path)):
        print(" " * i, path[i])
