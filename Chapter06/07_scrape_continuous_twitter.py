from selenium import webdriver
import time

driver = webdriver.PhantomJS()

print("Starting")
driver.get("https://twitter.com")
scroll_pause_time = 1.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    print(last_height)
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(scroll_pause_time)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    print(new_height, last_height)

    if new_height == last_height:
        break
    last_height = new_height