from os.path import expanduser
import const
from core.file_blob_writer import FileBlobWriter
from core.image_thumbnail_generator import ImageThumbnailGenerator
from util.urls import URLUtility

# download the image and get the bytes
img_data = URLUtility(const.ApodEclipseImage()).data

# we will store this in our home folder
fw = FileBlobWriter(expanduser("~"))

# Create a thumbnail generator and scale the image
tg = ImageThumbnailGenerator(img_data).scale(200, 200)

# write the image to a file
fw.write("eclipse_thumbnail.png", tg.bytes)
