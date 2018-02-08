from core.website_screenshot_with_screenshotapi import WebsiteScreenshotGenerator
from core.file_blob_writer import FileBlobWriter
from os.path import expanduser

# get the screenshot
image_bytes = WebsiteScreenshotGenerator("bd17a1e1-db43-4686-9f9b-b72b67a5535e")\
    .capture("http://espn.go.com", 500, 500).image_bytes

# save it to a file
FileBlobWriter(expanduser("~")).write("website_screenshot.png", image_bytes)
