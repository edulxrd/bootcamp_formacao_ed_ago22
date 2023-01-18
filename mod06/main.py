#%%

import selenium
from selenium import webdriver
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#%%
cep = input()

if cep:
    #Para iniciar o navegador já com o selenium
    driver = selenium.webdriver.Chrome()

    #%%
    # driver.get('https://howedu.com.br')

    #Dentro do site que abriu, vamos inspecionar o elemento de algum botão, e copiar com Xpath
    #Com esse comando dentro do site vamos realizar uma ação de click no botão que pegamos o Xpath
    # driver.find_element("xpath", '//*[@id="btn-config"]/div/div/a/span/span[2]').click()
    # driver.find_element("xpath", '//*[@id="adopt-accept-all-button"]').click()

    #%% Preenchendo formularios

    driver.get('https://buscacepinter.correios.com.br/app/endereco/index.php?t')

    #Criando uma variavel que ira receber o find element
    elem_cep = driver.find_element("name", 'endereco')

    #%%
    elem_cep.send_keys('04194-260') # Inserindo dados no elemento

    #%% 
    elem_cep = driver.find_element("name", 'tipoCEP')
    elem_cep.click()
    driver.find_element("xpath", '//*[@id="tipoCEP"]/optgroup/option[1]').click()

    # %%
    driver.find_element("id", 'btn_pesquisar').click()

    #%% Capturando dados com o selenium
    #Criamos uma linha para quando o botão de nova busca já estiver disponivel para clicar dar continuidade no codigo
    if WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn_nbusca"]'))): 
        logradouro = driver.find_element(
            "xpath", '/html/body/main/form/div[1]/div[2]/div/div[4]/table/tbody/tr/td[1]').text
        bairro = driver.find_element(
            "xpath", '/html/body/main/form/div[1]/div[2]/div/div[4]/table/tbody/tr/td[2]').text
        localidade = driver.find_element(
            "xpath", '/html/body/main/form/div[1]/div[2]/div/div[4]/table/tbody/tr/td[3]').text
    
    driver.close() # para não deixar o navegador aberto no final

    print("""
          Para o cep {} Temos:
          
          Endereço: {}
          Bairro: {}
          Localidade: {}
          """.format(
              cep,
              logradouro,
              bairro,
              localidade
          ))
          

    # %%
