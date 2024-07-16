from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time

def fechar_popup(driver):
    try:
        popup = driver.find_element("xpath", "//div[@class='fancybox-overlay fancybox-overlay-fixed')]")
        if popup:
            search_button = driver.find_element("xpath", "//button[@class='fancybox-item fancybox-close')]")
            search_button.click()
            time.sleep(1)
            print("Pop-up fechada.")
        else:
            print("Nenhuma pop-up encontrada.")
    except Exception as e:
        print(f"Erro ao tentar fechar a pop-up: {e}")

url = "https://apnews.com/"

# Função para pedir um parâmetro ao usuário
def definir_frase():
    frase = input("Por favor, informe oque deseja pesquisar: ")
    return frase
frase = definir_frase()

categorias = {
    "Featured Articles": "00000190-08f3-d7b0-a1fa-d9f37cb90000",
    "Live Blogs": "00000190-0dc5-d7b0-a1fa-dde7ec030000",
    "Photo Galleries": "0000018e-775a-d056-adcf-f75a7d350000",
    "Sections": "00000189-9323-dce2-ad8f-bbe74c770000",
    "Stories": "00000188-f942-d221-a78c-f9570e360000",
    "Subsections": "00000189-9323-db0a-a7f9-9b7fb64a0000",
    "Videos": "00000188-d597-dc35-ab8d-d7bf1ce10000"
}

while True:
    categoria_escolhida = input("Informe a categoria desejada: ")
    numero_associado = categorias.get(categoria_escolhida)

    if numero_associado:
        print(f"Aguarde enquanto a categoria {categoria_escolhida} é carregada.")
        break
    else:
        print("Categoria inválida. Por favor, tente novamente.")

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
search_input.send_keys(frase)
search_input.send_keys(u'\ue007')
time.sleep(5)

def scroll_down():
    driver.execute_script("window.scrollBy(0, 300);")

for _ in range(1):
    scroll_down()

fechar_popup(driver)
search_button = driver.find_element("xpath", "//bsp-toggler[@class='SearchFilter-content']")
search_button.click()
time.sleep(1)

fechar_popup(driver)
search_button = driver.find_element("xpath", "//button[@class='SearchFilter-seeAll-button']")
search_button.click()
time.sleep(2)

fechar_popup(driver)
checkbox = driver.find_element("xpath", f"//input[@type='checkbox' and @value='{numero_associado}']")
checkbox.click()
time.sleep(2)

fechar_popup(driver)
dropdown = Select(driver.find_element("xpath", "//select[@name='s' and contains(@class, 'Select-input')]"))
dropdown.select_by_visible_text("Newest")

time.sleep(120)
fechar_popup(driver)