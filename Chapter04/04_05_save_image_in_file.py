""" Demonstrate saving a downloaded url in a file """
from os.path import expanduser

import const
from core.file_blob_writer import FileBlobWriter
from util.urls import URLUtility

# download the image
item = URLUtility(const.ApodEclipseImage())

# create a file writer to write the data
FileBlobWriter(expanduser("~")).write(item.filename, item.data)

