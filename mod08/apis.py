import datetime
from abc import ABC, abstractmethod
import logging
import ratelimit
import requests
from backoff import on_exception, expo

#%%
#Criando um logger para criar um log 
# Level = o tipo de informação que queremos obter, no caso info são todas
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

#%% 
class mercadobitcoin(ABC):
    def __init__(self, moeda: str) -> None:
        self.moeda = moeda
        self.comecolink = 'https://www.mercadobitcoin.net/api'
 
    # Metodos com o nome começando com _ não ficam exposto para pessoa de fora 
    # @abstractmethod PARA OBRIGAR A ESTENDER A CLASSE não deixando fazer alterações


## **kargs - python entende que a assinatura dessa funcao pode receber qualquer argumento do tipo chave / valor
    @abstractmethod
    def _get_endpoint(self, **kargs) -> str:
        pass

    #response = resposta da API
    # response.raise_for_status() para verificar se o chamado foi efetuado com sucesso // .json() para retornar a responta em JSON
    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=29, period=30)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
    def get_data(self, **kargs) -> dict:
        endpoint = self._get_endpoint(**kargs)
        logger.info(f"Getting data from endpoint: {endpoint}")
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

class DaySummaryAPI(mercadobitcoin):
    type = "day-summary"
    def _get_endpoint(self, date: datetime.date) -> str:
        return (f'{self.comecolink}/{self.moeda}/{self.type}/{date.year}/{date.month}/{date.day}')
    
## print(DaySummaryAPI(moeda='BTC').get_data(date=datetime.date(2021, 6, 21)))



#%%
## unix_date_from = Converter uma data em unix
class tradesapi(mercadobitcoin):
    type = "trades"
    def _get_unix_epoch(self, date: datetime) -> int:
        return int(date.timestamp())

    def _get_endpoint(self, date_from: datetime.datetime = None, date_to: datetime.datetime = None) -> str:
        
        if date_from and not date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            endpoint = (f'{self.comecolink}/{self.moeda}/{self.type}/{unix_date_from}')

        elif date_from and date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            unix_date_to = self._get_unix_epoch(date_to)
            endpoint = (f'{self.comecolink}/{self.moeda}/{self.type}/{unix_date_from}/{unix_date_to}')
            if date_from > date_to:
                raise RuntimeError("Data inicial maior que a final")
        else:
            endpoint = (f'{self.comecolink}/{self.moeda}/{self.type}')
        
        return endpoint

# print (tradesapi("BTC").get_data(date_from=datetime.datetime(2021, 4, 29)))
# print (tradesapi("BTC").get_data(date_from=datetime.datetime(2021, 4, 29), date_to=datetime.datetime(2022, 4, 29)))
