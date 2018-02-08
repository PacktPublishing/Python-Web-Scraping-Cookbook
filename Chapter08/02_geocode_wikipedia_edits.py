from bs4 import BeautifulSoup
import requests
import json

def get_history_ips(article_title, limit):
    history_page_url = "https://en.wikipedia.org/w/index.php?title=%s&offset=&limit=%s&action=history" % (article_title, limit)
    print("Reading page: " + history_page_url)
    html = requests.get(history_page_url).text
    soup = BeautifulSoup(html, "lxml")

    anon_ip_anchors = soup.findAll("a", {"class": "mw-anonuserlink"})
    addresses = set()
    for ip in anon_ip_anchors:
        addresses.add(ip.get_text())
    return addresses

def get_geo_ips(ip_addresses):
    geo_ips = []
    for ip in ip_addresses:
        raw_json = requests.get("http://www.freegeoip.net/json/%s" % ip).text
        parsed = json.loads(raw_json)
        geo_ips.append(parsed)
    return geo_ips

def collect_geo_ips(article_title, limit):
    ip_addresses = get_history_ips(article_title, limit)
    print("Got %s ip addresses" % len(ip_addresses))
    geo_ips = get_geo_ips(ip_addresses)
    return geo_ips

if __name__ == "__main__":
    geo_ips = collect_geo_ips('Web_scraping', 500)
    for geo_ip in geo_ips:
        print(geo_ip)
    with open('geo_ips.json', 'w') as outfile:
        json.dump(geo_ips, outfile)
