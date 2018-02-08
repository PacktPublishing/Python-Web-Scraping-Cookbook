""" Demonstrate reading an image and reporting it's size """

import const
from util.urls import URLUtility

util = URLUtility(const.ApodEclipseImage())
print(len(util.data))
