""" Demonstrate saving a downloaded url in a file """

from core.s3_blob_writer import S3BlobWriter
from util.urls import URLUtility
import const

# download the image
item = URLUtility(const.ApodEclipseImage())

# store it in S3
S3BlobWriter(bucket_name="scraping-apod-images").write(item.filename, item.data)



