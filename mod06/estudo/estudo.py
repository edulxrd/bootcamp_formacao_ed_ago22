#%%
from selenium import webdriver
import time
import pandas as pd

#%%
driver = webdriver.Chrome()
driver.get('https://pt.wikipedia.org/wiki/Playboi_Carti')
driver.implicitly_wait(10)

tabela = driver.find_element(
    "xpath", '//*[@id="mw-content-text"]/div[1]/div[3]')
driver.close()

#%%
df = pd.read_html('<table>' + tabela.get_attribute('innerHTML') + '</table>')[0]

# %%
df.to_csv('Bibliografia Carti.csv', sep = ';', index = False)
# %%
df.rename(
    columns={'[Esconder]vdePlayboi Carti' : 'Tipo', '[Esconder]vdePlayboi Carti.1' : 'Discografia'},
    inplace=True
)
# %%
df = df.drop(0)
# %%
info = driver.find_element(
    "xpath", '//*[@id="mw-content-text"]/div[1]/table')
df2 = pd.read_html('<table>' + info.get_attribute('innerHTML') + '</table>')[0]

# %%
df2.loc[14, 'Playboi Carti.1'] = "Kanye West, A$AP Rocky, Kid Cudi, Lil Uzi Vert, Iggy Azalea, Trippie Redd"
df2
# %%
df2.loc[15, 'Playboi Carti.1'] = "www.playboicarti.com"
df2
# %%
df2 = df2.drop(0)
df2

#%%
df2.rename(
    columns={'Playboi Carti': '', 'Playboi Carti.1': ''},
    inplace=True
)
#%%
df2.to_csv('Infos Carti.csv', sep = ';', index=False)
df2
#
# %%
