#%%
# imports
from tkinter import E, EXCEPTION
import requests
import json
import logging

#%%
url = 'https://economia.awesomeapi.com.br/json/last/BTC-BRL'
ret = requests.get(url)
# %%
#ret.text para mostrar o codigo da pagina em texto

if ret:
    print(ret.text)
else:
    print('Falhou')
# %%
#json.loads carregar o texto com json

dolar = json.loads(ret.text)['BTCBRL']

# %%
# Criamos uma variavel para fazer o calculo de quanto é um valor pelo atual valor do dolar hoje
#bid = cotação dolar

print( f" 20 Dólares hoje custam {float(dolar['bid']) *20} reais")

# %%
#Replace para subistituir o '-' que existe no link da API por nada
#[:3] vetor para mostrar apenas os 3 PRIMEIROS digitos
#[-3: para contar os digitos de tras pra frente = PARA NÃO APARECER O NOME DA PRIMEIRA MOEDA 

def cotacao(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/json/last/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-','')]
    print( f" {valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor} {moeda[-3:]}")
    
    
# %%
# 20 = VALOR // 'BTC-BRL' = MOEDA
cotacao(20, 'BTC-BRL')

# %%
# try = tente fazer isso // except: pass = se não rodar continuar

try:
    cotacao(20, 'edu-BRL')
except:
    pass
    
# %%
# except Exception as e: mostrar onde esta o erro do codigo

try:
    cotacao(20, 'edu-BRL')
except Exception as a:
    print(a)
else:
    print('ok')
# %%
# Tratar erros de toda uma função
#except é a excessão, basicamente o erro
# Função onde passo valor, ele captura o valor e me retorna as moedas 
# def = definir uma função


def multi_moedas(valor, moeda):
    lst_money = ["USD-BRL",
                "EUR-BRL",
                "EDU-BRL",
                "BTC-BRL"
    ]
    valor = 20
    for moeda in lst_money:
            url = f'https://economia.awesomeapi.com.br/json/last/{moeda}'
            ret = requests.get(url)
            dolar = json.loads(ret.text)[moeda.replace('-','')]
            print( 
                  f" {valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor} {moeda[-3:]}")

#%%
lst_money = [
    "USD-BRL",
    "EUR-BRL",
    "EDU-BRL",
    "BTC-BRL"
]


multi_moedas(20, "BTC-BRL")
# %%
# Usar decorador, quando a gente quer usar uma função como decoradora de outra vamos usar a primera def
# do decorador com @, '@error_check'
# Isso vai fazer com que para a função multi_moedas execute ele passe primeiro pelo decorador error_check
# O Decorador vai capturar a função e criando uma outra função que valida se todos os parametros estão ok e 
# *args, **kargs puxa todos os argumentos de uma função
# func uma funcão como atributo de uma def (função)


def error_check(func):
    def inner_func(*args, **kargs):
        try:
            func(*args, **kargs)
        except:
            print(f"{func.__name__} falhou")
    return inner_func

@error_check
def multi_moedas(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/json/last/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-','')]
    print( 
            f" {valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor} {moeda[-3:]}")


#%%

multi_moedas(20,"USD-BRL")
multi_moedas(20,"EUR-BRL")
multi_moedas(20,"EDU-BRL")
multi_moedas(20,"BTC-BRL")
        

# %%
# exemplo backoff
# Raise = gerar uma excessão
# max_tries=10 = maximo de tentativas
# @backoff.on_exception(backoff.expo = decorador do backoff. Expoe todas as falhas que podem acontecer


import backoff
import random

@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=10)
def test_func(*args, **kargs):
    rnd = random.random()
    print(f"""
          RND: {rnd}
          args: {args if args else 'sem args'}
          kargs: {kargs if kargs else 'sem kargs'}
          """)
    if rnd < .2:
        raise ConnectionAbortedError('Conexão foi finalizada!')
    elif rnd < .4:
        raise ConnectionRefusedError('Conexão foi recusada')
    elif rnd < .8:
        raise TimeoutError('Tempo de espera excedido')
    else:
        return "ok"
        
# %%
test_func()

# %%
import logging

# %%
# Criando logs = log = logging.getLogger()
#log.setLevel(logging.DEBUG) = tipo de logging que queremos
# Formatter = Dar um formato. 
# asctime = hora, dia, mes,etc. Name = Nome do usario
# Level = nivel da minha informação. message = mensagem
# StreamHandler = jogar a log no terminal

log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s | %(name)s | %(levelname)s | %(message)s")
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)


# %%

@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=10)
def test_func(*args, **kargs):
    rnd = random.random()
    log.debug(f" RND: {rnd}")
    log.info(f"args: {args if args else 'sem args'}")
    log.info(f"kargs: {kargs if kargs else 'sem kargs'}")
    if rnd < .2:
        log.error('Conexão foi finalizada!')
        raise ConnectionAbortedError('Conexão foi finalizada!')
    elif rnd < .4:
        log.error('Conexão foi recusada!')
        raise ConnectionRefusedError('Conexão foi recusada')
    elif rnd < .6:
        log.error('Tempo de espera excedido')
        raise TimeoutError('Tempo de espera excedido')
    else:
        return "ok"
# %%
test_func()
# %%

