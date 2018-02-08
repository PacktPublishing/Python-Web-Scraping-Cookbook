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

    plt.figure(figsize=(10,8))

    node_positions = nx.spring_layout(g)

    nx.draw_networkx_nodes(g, node_positions, g.nodes, node_color='green', node_size=50)
    nx.draw_networkx_edges(g, node_positions)

    labels = { node: node for node in g.nodes() }
    nx.draw_networkx_labels(g, node_positions, labels, font_size=9.5)

    plt.show()
