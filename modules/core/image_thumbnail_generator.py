import io
from PIL import Image

class ImageThumbnailGenerator():
    def __init__(self, bytes):
        # Create a pillow image with the data provided
        self._image = Image.open(io.BytesIO(bytes))

    def scale(self, width, height):
        # call the thumbnail method to create the thumbnail
        self._image.thumbnail((width, height))
        return self

    @property
    def bytes(self):
        # returns the bytes of the pillow image

        # save the image to an in memory objects
        bytesio = io.BytesIO()
        self._image.save(bytesio, format="png")

        # set the position on the stream to 0 and return the underlying data
        bytesio.seek(0)
        return bytesio.getvalue()


