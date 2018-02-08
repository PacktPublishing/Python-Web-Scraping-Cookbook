from reppy.robots import Robots

url = "http://www.amazon.com"
robots = Robots.fetch(url + "/robots.txt")
paths = [
    '/',
    '/gp/dmusic/',
    '/gp/dmusic/promotions/PrimeMusic/',
    '/gp/registry/wishlist/'
]

for path in paths:
    print("{0}: {1}".format(robots.allowed(path, '*'), url + path))

