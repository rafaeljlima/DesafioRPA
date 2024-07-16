from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def fechar_popup(driver):
    try:
        popup = driver.find_elements("xpath", "//div[contains(@class, 'fancybox-overlay fancybox-overlay-fixed')]")
        if popup:
            close_button = driver.find_element("xpath", "//button[contains(@class, 'fancybox-item fancybox-close')]")
            close_button.click()
            time.sleep(1)
            print("Pop-up fechada.")
        else:
            print("Nenhuma pop-up encontrada.")
    except Exception as e:
        print(f"Erro ao tentar fechar a pop-up: {e}")

url = "https://apnews.com/"

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(url)
driver.maximize_window() 

fechar_popup(driver)
search_button = driver.find_element("xpath", "//button[@class='SearchOverlay-search-button']")
search_button.click()

time.sleep(2)

fechar_popup(driver)
search_input = driver.find_element("xpath", "//label[@class='SearchOverlay-search-label']")
search_input.send_keys("Olympic Games")
search_input.send_keys(u'\ue007')

time.sleep(60)

fechar_popup(driver)