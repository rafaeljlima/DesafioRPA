from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

url = "https://apnews.com/"

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(url)
driver.maximize_window() 

search_button = driver.find_element("xpath", "//button[@class='SearchOverlay-search-button']")
search_button.click()

time.sleep(1)

search_input = driver.find_element("xpath", "//label[@class='SearchOverlay-search-label']")
search_input.send_keys("Olympic Games")
search_input.send_keys(u'\ue007')

time.sleep(2)