"""This module provides helpers for reading URLs and determining content types"""

import urllib.request
from urllib.parse import urlparse
import os
import const

class URLUtility:
    """ This class provides utility functions to make working with URL's and data easier """
    def __init__(self, url, readNow=True):
        """ Construct the object, parse the URL, and download now if specified"""
        self._url = url
        self._response = None
        self._parsed = urlparse(url)
        if readNow:
            self.read()

    def read(self):
        print('Reading URL: ' + self._url)
        self._response = urllib.request.urlopen(self._url)
        self._data = self._response.read()
        print("Read {0} bytes".format(len(self._data)))

    def ensure_response(self):
        if self._response is None:
            self.read()

    @property
    def data(self):
        self.ensure_response()
        return self._data
        
    @property
    def filename_without_ext(self):
        filename = os.path.splitext(os.path.basename(self._parsed.path))[0]
        return filename

    @property
    def contenttype(self):
        self.ensure_response()
        return self._response.headers['content-type']

    @property
    def extension_from_contenttype(self):
        self.ensure_response()

        map = const.ContentTypeToExtensions()
        if self.contenttype in map:
            return map[self.contenttype]
        print("Content type not found: " + self.contenttype)
        return None

    @property
    def extension_from_url(self):
        ext = os.path.splitext(os.path.basename(self._parsed.path))[1]
        return ext

    @property
    def filename(self):
        return self.filename_without_ext + self.extension_from_contenttype

    @property
    def response_headers(self):
        return self._response.headers

    @property
    def response(self):
        return self._response

if __name__ == "__main__":
    u = URLUtility("https://apod.nasa.gov/apod/image/1709/2017O1&2015ER61_170917_2400_clean.jpg")
    u.read()
    print(u.contenttype)
    print(u.filename_base)
    print(u.extension)