from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bert import *

driver = webdriver.Firefox(
    executable_path=r"/usr/local/bin/geckodriver-v0.29.1-linux64/geckodriver"
)
driver.get("https://nvd.nist.gov/vuln/search")

driver.find_element_by_name("query").send_keys("information security")
time.sleep(3)
driver.find_element_by_id("vuln-search-submit").click()
time.sleep(5)
for tr in driver.find_elements_by_id("row"):
    tds = tr.find_elements_by_tag_name("td")
    for td in tds:
        bert(td.text)

# driver.close()
print("sample test case successfully completed")