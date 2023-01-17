#%%
from multiprocessing.heap import Arena
from string import octdigits
from wsgiref.validate import validator
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd



# %%

url = 'https://www.vivareal.com.br/venda/parana/curitiba/apartamento_residencial/?pagina={}'
# %%

i = 1 
ret = requests.get(url.format(i))
soup = bs(ret.text)

# %%
soup
# %%
# a = link
# soup.find_all (tipo da linha, classe da linha)
# text.replace('.','') repondo o ponto por nada para não entender como virgula
# float(soup.find para tranformar o texto em numeros

houses = soup.find_all(
    'a', {'class' :'property-card__content-link js-card-title'})
qtd_imoveis = float(soup.find('strong', {'class' : 'results-summary__count js-total-records'}).text.replace('.',''))
# %%
len(houses)
# %%
qtd_imoveis /36

# %%
house = houses[0]


# %%
house
# %%
# strip() para excluir os espaços que ficam no começo e no final
df = pd.DataFrame(
    columns=[
        'descricao',
        'endereco',
        'Area',
        'quartos',
        'wc',
        'vagas',
        'valor', 
        'condominio',
        'link',
    
    ]
)

#%%
i = 0

#%%
#  df.loc[df.shape[0]] = pegar ultima posição
#  while qtd_imoveis > df.shape[0] = enquanto eu não tiver imoveis suficientes que
#  a mesma quantidade do total que o site está dando

while qtd_imoveis > df.shape[0]:
    i += 1 
    print (f"Valor de i: {i} \t\t qtd_imoveis: {df.shape[0]}")
    ret = requests.get(url.format(i))
    soup = bs(ret.text, features="html.parser")
    houses = soup.find_all(
    'a', {'class' :'property-card__content-link js-card-title'})
    
    for house in houses:
        try:
            descricao = house.find('span',{'class': 'property-card__title'}).text.strip()
        except:
            descricao = None    
        try:
            endereco = house.find('span',{'class': 'property-card__address'}).text.strip()
        except:
            endereco = None    
        try:
            Area = house.find('span',{'class': 'property-card__detail-value'}).text.strip()
        except:
            Area = None    
        try:
            quartos = house.find('li',{'class': 'property-card__detail-room'}).span.text.strip()
        except:
            quartos = None    
        try:
            wc  = house.find('li',{'class': 'property-card__detail-bathroom'}).span.text.strip()
        except:
            wc  = None    
        try:
            vagas = house.find('li',{'class': 'property-card__detail-garage'}).span.text.strip()
        except:
            vagas = None    
        try:
            valor = house.find('div',{'class': 'property-card__price'}).p.text.strip()
        except:
            valor = None    
        try:
            condominio = house.find('strong',{'class': 'js-condo-price'}).text.strip()
        except:
            condominio = None    
        try:
            link = 'https://www.vivareal.com.br' + house['href']
        except:
            link = None    
            
            
                                                        
        df.loc[df.shape[0]] = [
            descricao,
            endereco,
            Area,
            quartos,
            wc,
            vagas,
            valor, 
            condominio,
            link,
        ]
#%%
print (descricao)
print (endereco)
print (f'{Area} m²')
print (f'{quartos} Quartos')
print (f'{wc} Banheiros')
print (f'{vagas} Vagas')
print (valor)
print (f'Condominio = {condominio}')
print (link)


#%%
df.to_csv('banco_de_imoveis.csv', sep=';', index=False)
# %%


# %%
