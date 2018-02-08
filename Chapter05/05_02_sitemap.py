import sitemap

map = sitemap.get_sitemap("https://www.nasa.gov/sitemap.xml")
url_info = sitemap.parse_sitemap(map)
print("Found {0} urls".format(len(url_info)))
for u in url_info[0:10]:
    print(u)


