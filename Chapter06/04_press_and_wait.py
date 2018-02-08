from selenium import webdriver
from selenium.webdriver.support import ui

driver = webdriver.PhantomJS()
driver.get("http://the-internet.herokuapp.com/dynamic_loading/2")
button = driver.find_element_by_xpath("//*/div[@id='start']/button")
button.click()
print("clicked")
wait = ui.WebDriverWait(driver, 10)
wait.until(lambda driver: driver.find_element_by_xpath("//*/div[@id='finish']"))
finish_element=driver.find_element_by_xpath("//*/div[@id='finish']/h4")
print(finish_element.text)
