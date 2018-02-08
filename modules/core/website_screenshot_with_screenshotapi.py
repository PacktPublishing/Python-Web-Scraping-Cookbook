import sys
import urllib
import requests
import json
import time
import io
from PIL import Image

class WebsiteScreenshotGenerator:
    def __init__(self, apikey):
        self._screenshot = None
        self._apikey = apikey

    def capture(self, url, width, height, crop=True):
        key = self.beginCapture(url, "{0}x{1}".format(width, height), "true", "firefox", "true")

        print("The image key is: " + key)

        timeout = 30
        tCounter = 0
        tCountIncr = 3

        while True:
            result = self.tryRetrieve(key)
            if result["success"]:
                print("Saving screenshot to: downloaded_screenshot.png" + key)

                bytes=result["bytes"]
                self._screenshot = Image.open(io.BytesIO(bytes))

                if crop:
                    # crop the image
                    self._screenshot = self._screenshot.crop((0, 0, width, height))
                    print("Cropped the image to: {0} {1}".format(width, height))
                break

            tCounter += tCountIncr
            print("Screenshot not yet ready.. waiting for: " + str(tCountIncr) + " seconds.")
            time.sleep(tCountIncr)
            if tCounter > timeout:
                print("Timed out while downloading: " + key)
                break
        return self

    def beginCapture(self, url, viewport, fullpage, webdriver, javascript):
        serverUrl = "https://api.screenshotapi.io/capture"
        print('Sending request: ' + url)
        headers = {'apikey': self._apikey}
        params = {'url': urllib.parse.unquote(url).encode('utf8'), 'viewport': viewport, 'fullpage': fullpage,
                  'webdriver': webdriver, 'javascript': javascript}
        result = requests.post(serverUrl, data=params, headers=headers)
        print(result.text)
        json_results = json.loads(result.text)
        return json_results['key']


    def tryRetrieve(self, key):
        url = 'https://api.screenshotapi.io/retrieve'
        headers = {'apikey': self._apikey}
        params = {'key': key}
        print('Trying to retrieve: ' + url)
        result = requests.get(url, params=params, headers=headers)

        json_results = json.loads(result.text)
        if json_results["status"] == "ready":
            print('Downloading image: ' + json_results["imageUrl"])
            image_result = requests.get(json_results["imageUrl"])
            return {'success': True, 'bytes': image_result.content}
        else:
            return {'success': False}

    @property
    def image(self):
        return self._screenshot

    @property
    def image_bytes(self):
        bytesio = io.BytesIO()
        self._screenshot.save(bytesio, "PNG")
        bytesio.seek(0)
        return bytesio.getvalue()
