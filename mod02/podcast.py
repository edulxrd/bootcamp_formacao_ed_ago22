#%%
# Organizar dados de uma pagina. BeautifulSoup mostra a melhor parser para se utilizar 
# na pagina. Com o comando soup = bs(ret.text), ret.text sendo a variavel da URL

import requests
from bs4 import BeautifulSoup as bs
import logging
import pandas as pd

# %%
url = 'https://portalcafebrasil.com.br/todos/podcasts/'

# %%
ret = requests.get(url)

# %%
ret.text

# %%
soup = bs(ret.text)

# %%
soup

# %%
# Achar dentro do codigo fonte a informação, nesse caso h5 é o titulo do primeiro podcast do site
soup.find('h5')

# %%
# Sem o link, somente o texto
soup.find('h5').text

# %%
# Mostrar somente o link
soup.find('h5').a['href']

# %%
lst_podcast = soup.find_all('h5')

# %%
for item in lst_podcast:
    print(f"Episodio: {item.text} - Link {item.a['href']}")
# %%

url = 'https://portalcafebrasil.com.br/todos/podcasts/page/{}/?ajax=true'

# %%
url.format(5)
# %%
# Criando variavel com soup, ger_podcast irá puxar o link
# ret para requisições do URL
# soup = visualizar melhor parser
# return soup.find_all('h5') para mostrar tudo que o soup achou como h5 = titulo podcast

def get_podcast(url):
    ret = requests.get(url)
    soup = bs(ret.text)
    return soup.find_all('h5')
# %%
# url.formart para inserir um numero ou informação dentro do {} que está dentro da ulr
# (url.format(5) para ir para pagina 5
get_podcast(url.format(5))

#%%
# Sistema para abilitar o logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s | %(name)s | %(levelname)s | %(message)s")
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

# %%
# variavel de interação = i
# Comandos para rodar todas as paginas do site para pegar todos os links dos podcasts
#usando while
# len() = contar quantidade


i = 1
lst_podcast = []
lst_get = get_podcast(url.format(i))
log.debug(f"Coletados {len(lst_get)} episodios do link do {(url.format(i))}")
while len(lst_get) > 0:
    lst_podcast = lst_podcast + lst_get
    i += 1
    lst_get = get_podcast(url.format(i))
    log.debug(f"Coletados {len(lst_get)} episodios do link do {(url.format(i))}")

# %%
len(lst_podcast)

# %%
#rodando a função
lst_podcast

# %%
#df = dataframes, criados com panda
df = pd.DataFrame(columns=['nome', 'link'])

# %%
# df.loc localizar ultima posição do dataframe
# df.shape retorna as duas dimensões do dataframe, 0 sendo as linhas e 1 sendo coluna
# item.text = titulo do podcast
# item.a['href'] = link do podcast 

for item in lst_podcast:
    df.loc[df.shape[0]] = [item.text, item.a['href']]
    

# %%
# mostrar linhas / colunas
df.shape

# %% 
# Criamos um arquivo contendo o nome do podcast e o link utilizando pandas
# df.to_csv = Exportar um arquivo em formato csv
# 'Banco_de_podcast.csv' = nome que eu vou dar
# sep = separador, sempre usar ';'
# index = lista todos os itens da primeira coluna, colocar como false

df.to_csv('Banco_de_podcast.csv', sep=';', index=False)
# %%
