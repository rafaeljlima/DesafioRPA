from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#Definindo URL
url = "https://apnews.com/"

#Definindo a frase
def definir_frase():
    frase = input("Por favor, informe oque deseja pesquisar: ")
    return frase
frase = definir_frase()

#Dicionario de categorias
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
    #Exibindo as categorias
    print("Por favor escolha uma das seguintes categorias disponíveis:")
    for categoria in categorias:
        print(categoria)
    
    #Escolhendo a categoria
    categoria_escolhida = input("Informe a categoria desejada: ")
    numero_associado = categorias.get(categoria_escolhida)
    
    #Verificando se a categoria existe
    if numero_associado:
        print(f"Aguarde enquanto a categoria {categoria_escolhida} é carregada.")
        break
    else:
        print("Categoria inválida. Por favor, tente novamente.")

#Configurando Selenium
options = Options()
options.add_experimental_option("detach", True)

#Instanciando o WebDriver
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

#Acessando o site
driver.get(url)
driver.maximize_window() 

#Clicando no botão de pesquisa e enviando a frase
search_button = driver.find_element(By.CLASS_NAME, 'SearchOverlay-search-button').click()
time.sleep(2)
search_input = driver.find_element(By.CLASS_NAME, 'SearchOverlay-search-label')
search_input.send_keys(frase)
search_input.send_keys(u'\uE007')
time.sleep(2)

#Scroll para ver melhor os resultados
def scroll_down():
    driver.execute_script("window.scrollBy(0, 300);")
for _ in range(1):
    scroll_down()

#Abrindo o filtro e selecionando a opção do usuário
filter_wait = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'SearchFilter-content')))
filter_toggle = driver.find_element(By.CLASS_NAME, "SearchFilter-content").click()
time.sleep(1)
seeall_button = driver.find_element(By.CLASS_NAME, "SearchFilter-seeAll-button").click()
time.sleep(1)
checkbox = driver.find_element("xpath", f"//input[@type='checkbox' and @value='{numero_associado}']").click()

order_wait = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'Select-input')))
dropdown = Select(driver.find_element("xpath", "//select[@name='s' and contains(@class, 'Select-input')]"))
dropdown.select_by_visible_text("Newest")