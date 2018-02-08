""" Demonstrate determining extension from content type returned in response """
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import const
from util.urls import URLUtility

util = URLUtility(const.ApodEclipseImage())
print("The content type is: " + util.contenttype)
