from subprocess import Popen, PIPE
from selenium import webdriver
from PIL import Image
import io

class WebsiteScreenshotGenerator():
    def __init__(self):
        self._screenshot = None

    def capture(self, url, width, height, crop=True):
        print ("Capturing website screenshot of: " + url)
        driver = webdriver.PhantomJS()

        if width and height:
            driver.set_window_size(width, height)

        # go and get the content at the url
        driver.get(url)

        # get the screenshot and make it into a Pillow Image
        self._screenshot = Image.open(io.BytesIO(driver.get_screenshot_as_png()))
        print("Got a screenshot with the following dimensions: {0}".format(self._screenshot.size))

        if crop:
            # crop the image
            self._screenshot = self._screenshot.crop((0,0, width, height))
            print("Cropped the image to: {0} {1}".format(width, height))

        return self

    @property
    def image(self):
        return self._screenshot

    @property
    def image_bytes(self):
        bytesio = io.BytesIO()
        self._screenshot.save(bytesio, "PNG")
        bytesio.seek(0)
        return bytesio.getvalue()


if __name__ == "__main__":
    import const
    g = WebsiteScreenshotGenerator()
    #g.do_screen_capturing(const.ApodEclipsePage(), "/Users/michaelheydt/thumbnail.png", 500, 100)
    g.do_screen_capturing("http://espn.go.com", 500, 100)

    # need to explicitly crop