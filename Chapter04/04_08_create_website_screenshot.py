from core.website_screenshot_generator import  WebsiteScreenshotGenerator
from core.file_blob_writer import FileBlobWriter
from os.path import expanduser

# get the screenshot
image_bytes = WebsiteScreenshotGenerator().capture("http://espn.go.com", 500, 500).image_bytes

# save it to a file
FileBlobWriter(expanduser("~")).write("website_screenshot.png", image_bytes)
