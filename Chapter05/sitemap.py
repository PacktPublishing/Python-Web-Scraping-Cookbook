from bs4 import BeautifulSoup
import requests

def get_sitemap(url):
    get_url = requests.get(url)

    if get_url.status_code == 200:
        return get_url.text
    else:
        print ('Unable to fetch sitemap: %s.' % url)


def process_sitemap(s):
    soup = BeautifulSoup(s, "lxml")
    result = []

    for loc in soup.findAll('loc'):
        item = {}
        item['loc'] = loc.text
        item['tag'] = loc.parent.name
        if loc.parent.lastmod is not None:
            item['lastmod'] = loc.parent.lastmod.text
        if loc.parent.changeFreq is not None:
            item['changeFreq'] = loc.parent.changeFreq.text
        if loc.parent.priority is not None:
            item['priority'] = loc.parent.priority.text
        result.append(item)

    return result

def is_sub_sitemap(s):
    if s['loc'].endswith('.xml') and s['tag'] == 'sitemap':
        return True
    else:
        return False

def parse_sitemap(s):
    sitemap = process_sitemap(s)
    result = []

    while sitemap:
        candidate = sitemap.pop()

        if is_sub_sitemap(candidate):
            sub_sitemap = get_sitemap(candidate['loc'])
            for i in process_sitemap(sub_sitemap):
                sitemap.append(i)
        else:
            result.append(candidate)

    return result