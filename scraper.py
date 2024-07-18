from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

#Definindo URL
url = "https://www.latimes.com/"

#Definindo a pesquisa
def definir_frase():
    frase = input("Por favor, informe oque deseja pesquisar: ")
    return frase
frase = definir_frase()

def definir_topico():
    topico = input("Por favor, informe o topico da pesquisa: ")
    return topico
topico = definir_topico()

def definir_tipo():
    tipo = input("Por favor, informe o tipo de resultado: ")
    return tipo
tipo = definir_tipo()

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
search_button = driver.find_element(By.XPATH, "/html/body/ps-header/header/div[2]/button").click()
time.sleep(2)
search_input = driver.find_element(By.XPATH, "/html/body/ps-header/header/div[2]/div[2]/form/label/input")
search_input.send_keys(frase)
search_input.send_keys(u'\uE007')
time.sleep(2)

seeall_topics = driver.find_element("xpath", "/html/body/div[2]/ps-search-results-module/form/div[2]/ps-search-filters/div/aside/div/div[3]/div[1]/ps-toggler/ps-toggler/button").click()

#Abrindo o filtro e selecionando a opção do usuário
filter_wait = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'checkbox-input-element')))
listatopicos = driver.find_element(By.XPATH, '/html/body/div[2]/ps-search-results-module/form/div[2]/ps-search-filters/div/aside/div/div[3]/div[1]/ps-toggler/ps-toggler/div/ul')
filhos = listatopicos.find_elements(By.TAG_NAME, "li")

encontroutopico = 0
for filho in filhos:
    labelfilho = filho.find_element(By.TAG_NAME, "label")
    inputfilho = labelfilho.find_element(By.TAG_NAME, "input")
    spanfilho = labelfilho.find_element(By.TAG_NAME, "span")
    if spanfilho.text == topico:
        encontroutopico = 1
        inputfilho.click()
        break

if (encontroutopico == 0):
    print("nenhum topico foi encontrado")
    exit()
time.sleep(5)

dropdown = Select(driver.find_element("xpath", "//select[@name='s' and contains(@class, 'select-input')]"))
dropdown.select_by_visible_text("Newest")
time.sleep(5)

seeall_type = driver.find_element(By.XPATH, "/html/body/div[2]/ps-search-results-module/form/div[2]/ps-search-filters/div/aside/div/div[3]/div[2]/ps-toggler/ps-toggler/button").click()
time.sleep(5)

listatipo = driver.find_element(By.XPATH, '/html/body/div[2]/ps-search-results-module/form/div[2]/ps-search-filters/div/aside/div/div[3]/div[2]/ps-toggler/ps-toggler/div/ul')
filhos = listatipo.find_elements(By.TAG_NAME, "li")

encontroutipo = 0
for filho in filhos:
    labelfilho = filho.find_element(By.TAG_NAME, "label")
    inputfilho = labelfilho.find_element(By.TAG_NAME, "input")
    spanfilho = labelfilho.find_element(By.TAG_NAME, "span")
    if spanfilho.text == tipo:
        encontroutipo = 1
        inputfilho.click()
        break

if (encontroutipo == 0):
    print("nenhum tipo foi encontrado")
    exit()
time.sleep(5)

listanoticias = driver.find_element(By.XPATH, '/html/body/div[2]/ps-search-results-module/form/div[2]/ps-search-filters/div/main/ul')
filhos = listanoticias.find_elements(By.TAG_NAME, "li")

tituloslista = []
for filho in filhos:
    h3filho = filho.find_element(By.TAG_NAME, "h3")
    ahreffilho = h3filho.find_element(By.TAG_NAME, "a")
    tituloslista.append(ahreffilho.text)

dataslista = []
for filho in filhos:
    datafilho = filho.find_element(By.CLASS_NAME, 'promo-timestamp')
    dataslista.append(datafilho.text)

descricoeslista = []
valor_monetariolista = []
for filho in filhos:
    try:
        descricaofilho = filho.find_element(By.CLASS_NAME, 'promo-description').text
    except:
        descricaofilho = None
    descricoeslista.append(descricaofilho)

    valor_monetario = re.search(r'(\$\d+[\,*\d+]*\.*\d+|\d+\sdollars|\d+\sUSD)', descricaofilho)
    
    if valor_monetario:
        valor_monetariolista.append(valor_monetario.group())
    else:
        valor_monetariolista.append(None)