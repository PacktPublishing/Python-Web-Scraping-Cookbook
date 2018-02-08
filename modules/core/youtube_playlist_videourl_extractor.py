from bs4 import BeautifulSoup
from selenium import webdriver

class YouTubePlaylistVideoUrlExtractor():
    def __init__(self):
        self._urls = None
        pass

    def get(self, playlist_url):
        driver = webdriver.PhantomJS()
        driver.set_script_timeout(30)
        driver.get(playlist_url)
        html = driver.execute_script("return document.getElementsByTagName('html')[0].outerHTML")
        bsobj = BeautifulSoup(html, "lxml")
        anchors = bsobj.findAll("a", {"class": " spf-link playlist-video clearfix yt-uix-sessionlink spf-link "})
        self._urls = list(map(lambda a: "https://www.youtube.com" + a['href'], anchors))
        return self

    @property
    def urls(self):
        return self._urls

