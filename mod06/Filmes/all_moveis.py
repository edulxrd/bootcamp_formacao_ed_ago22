#%%
from selenium import webdriver
import time
import pandas as pd

#%%
driver = webdriver.Chrome()
driver.get('https://pt.wikipedia.org/wiki/Nicolas_Cage')
time.sleep(5)

#Serve para agurdar o o comando estar disponivel para ser executado, ele tenta, se não conseguir espera 10s
driver.implicitly_wait(10) 

#%%    
tabela = driver.find_element(
    "xpath", '//*[@id="mw-content-text"]/div[1]/table[2]')
#print (tabela.get_attribute('innerHTML')) #Para pegar o codigo HTML da linha da tabela

# %% Criando um dataframe para utilizar o pandar para formatar codigos HTML e criar um csv
#[0] serve para o df não ser uma lista // <table> porque nosso codigo HTML começa assim
df = pd.read_html('<table>' + tabela.get_attribute('innerHTML') + '</table>')[0] 

# %% Filtrando os filmes do ano de 1984
df[df['Ano']==1984]

#%% Criando arquivo csv
df.to_csv('Filmes_Cage.csv', sep=';', index=False)
            
#%% Print da tela
with open('print.png', 'wb') as f:
    f.write(driver.find_element("xpath", '/html/body/div[1]').screenshot_as_png)

#%% Outro metodo que não da sequencia no codigo equanto não encontrar o elemento 
#test_path = '//*[@id="menu-1-739815d"]/li[4]/a'
#def tem_intem(xpath, drive = driver):
#    try:
#        driver.find_element("xpath", xpath)
#        return True
#    except:
#        False
##%%        
#if tem_intem(test_path):
#    print('OK')
#while not tem_intem(test_path):
#    pass