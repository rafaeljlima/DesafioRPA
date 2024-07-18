from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime
import re
import pandas as pd

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

#Acessando o site
driver.get(url)
driver.maximize_window()

#Clicando no botão de pesquisa e enviando a frase
botao_pesquisa = driver.find_element(By.XPATH, "/html/body/ps-header/header/div[2]/button").click()
time.sleep(2)
input_pesquisa = driver.find_element(By.XPATH, "/html/body/ps-header/header/div[2]/div[2]/form/label/input")
input_pesquisa.send_keys(frase)
input_pesquisa.send_keys(u'\uE007')
time.sleep(8)

#Expandindo os topicos
seeall_topico = driver.find_element(By.XPATH, "/html/body/div[2]/ps-search-results-module/form/div[2]/ps-search-filters/div/aside/div/div[3]/div[1]/ps-toggler/ps-toggler/button" or "/html/body/div[3]/ps-search-results-module/form/div[2]/ps-search-filters/div/aside/div/div[3]/div[1]/ps-toggler/ps-toggler/button").click()

#Procurando o topico e selecionando a opção do usuário
time.sleep(5)
listatopicos = driver.find_element(By.XPATH, '/html/body/div[2]/ps-search-results-module/form/div[2]/ps-search-filters/div/aside/div/div[3]/div[1]/ps-toggler/ps-toggler/div/ul' or '/html/body/div[3]/ps-search-results-module/form/div[2]/ps-search-filters/div/aside/div/div[3]/div[1]/ps-toggler/ps-toggler/div/ul')
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
time.sleep(8)

#Selecionando noticias mais recentes
dropdown = Select(driver.find_element("xpath", "//select[@name='s' and contains(@class, 'select-input')]"))
dropdown.select_by_visible_text("Newest")
time.sleep(8)

#Expandindo os tipos
seeall_tipo = driver.find_element(By.XPATH, "/html/body/div[2]/ps-search-results-module/form/div[2]/ps-search-filters/div/aside/div/div[3]/div[2]/ps-toggler/ps-toggler/button" or "/html/body/div[3]/ps-search-results-module/form/div[2]/ps-search-filters/div/aside/div/div[3]/div[2]/ps-toggler/ps-toggler/button").click()

#Procurando o tipo e selecionando a opção do usuário
listatipo = driver.find_element(By.XPATH, '/html/body/div[2]/ps-search-results-module/form/div[2]/ps-search-filters/div/aside/div/div[3]/div[2]/ps-toggler/ps-toggler/div/ul' or '/html/body/div[3]/ps-search-results-module/form/div[2]/ps-search-filters/div/aside/div/div[3]/div[2]/ps-toggler/ps-toggler/div/ul')
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
time.sleep(8)

#Definindo a data atual
data_atual = datetime.now()
mes_anterior = data_atual.month - 1 if data_atual.month > 1 else 12
ano_mes_anterior = data_atual.year if data_atual.month > 1 else data_atual.year - 1

#Abrindo listas para receber os dados
tituloslista = []
dataslista = []
descricoeslista = []
valor_monetariolista = []

def coletar_noticias():
    global tituloslista, dataslista, descricoeslista, valor_monetariolista

    time.sleep(5)
    #Definindo o ul e li que recebem as notícias
    listanoticias = driver.find_element(By.CLASS_NAME, "search-results-module-results-menu")
    filhos = listanoticias.find_elements(By.TAG_NAME, "li")

    #Repetição para capturar as informaçoes das notícias
    for filho in filhos:
        datafilho = filho.find_element(By.CLASS_NAME, 'promo-timestamp').text
        try:
            datafilho_datetime = datetime.strptime(datafilho, '%B %d, %Y')
        except ValueError:
            print(f"Erro ao converter a data: {datafilho}")
            continue

        #Condição para verificar se a data é do mês atual ou mês passado
        if(datafilho_datetime.year == data_atual.year and datafilho_datetime.month == data_atual.month) or (datafilho_datetime.year == ano_mes_anterior and datafilho_datetime.month == mes_anterior):
            #Inserindo dados nas listas
            h3filho = filho.find_element(By.TAG_NAME, "h3")
            ahreffilho = h3filho.find_element(By.TAG_NAME, "a")
            tituloslista.append(ahreffilho.text)
            dataslista.append(datafilho)

            #Inserindo descrição caso tenha
            try:
                descricaofilho = filho.find_element(By.CLASS_NAME, 'promo-description').text
            except:
                descricaofilho = None
            descricoeslista.append(descricaofilho)

            #Inserindo valor monetário caso tenha
            valor_monetario = re.search(r'(\$\d+[\,*\d+]*\.*\d*|\d+\sdollars|\d+\sUSD)', descricaofilho)
            if valor_monetario:
                valor_monetariolista.append(valor_monetario.group())
            else:
                valor_monetariolista.append(None)
        else:
            return False
    return True
    
#Confição para verificar se precisa continuar coletando e passar de página    
while True:
    continuar_coletando = coletar_noticias()
    if not continuar_coletando:
        break

    try:
        botao_pagina = driver.find_element(By.CLASS_NAME, "search-results-module-next-page")
        botao_pagina.click()
        time.sleep(8)
    except:
        break

#Insertando dados na planilha
planilha = pd.DataFrame({'Titulo': tituloslista, 'Data': dataslista, 'Descrição': descricoeslista, 'Valor_monetário': valor_monetariolista})
planilha.to_excel('planilha.xlsx', index=False)
planilha.to_csv('planilha.csv', index=False)