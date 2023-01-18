import datetime
from unittest.mock import patch
import pytest
from apis import mercadobitcoin, DaySummaryAPI, tradesapi
import requests

#python -m pytest no terminar para executar o test
# Utilizaremos a bibli pytest
#Todo teste é uma função, para cada teste uma função diferente // Vamos testar o metodo get_endpoint

class TestDaySummaryAPI:
    #Parametrizando o teste para usar herança: ele recebe dois argumentos, 1° String (Nome dos argumentos)
    # 2° argumento é uma lista
    @pytest.mark.parametrize(
        "coin , date, expected",
        [
            ("BTC", datetime.date(2023, 1, 10), "https://www.mercadobitcoin.net/api/BTC/day-summary/2023/1/10"),
            ("ETH", datetime.date(2023, 1, 10), "https://www.mercadobitcoin.net/api/ETH/day-summary/2023/1/10"),
            ("ETH", datetime.date(2023, 1, 1), "https://www.mercadobitcoin.net/api/ETH/day-summary/2023/1/1")
        ]
    )
    def test_get_endpoint_api(self, coin, date, expected):
        api = DaySummaryAPI(moeda=coin)
        # Para pegarmos o valor real em testes, utilizamos o actual e chamamos o metodo
        actual = api._get_endpoint(date=date)
        # assert retorna TRUE se os dois forem iguais ou false se não
        assert actual == expected

# Criando um teste para Trade API
class TestTradeApi:
    @pytest.mark.parametrize(
        "coin, date_from, date_to, expected",
        [
            ("TEST", datetime.datetime(2023,1,9), datetime.datetime(2023,1,10), 
             "https://www.mercadobitcoin.net/api/TEST/trades/1673233200/1673319600"),
            ("TEST", datetime.datetime(2023,1,7), datetime.datetime(2023,1,8), 
             "https://www.mercadobitcoin.net/api/TEST/trades/1673060400/1673146800"),
            ("TEST", None, None, 
             "https://www.mercadobitcoin.net/api/TEST/trades"),
            ("TEST", None, datetime.datetime(2023,1,8), 
             "https://www.mercadobitcoin.net/api/TEST/trades"),
            ("TEST", datetime.datetime(2023,1,7), None,  
             "https://www.mercadobitcoin.net/api/TEST/trades/1673060400")
            
        ]
    )
    def test_get_endpoint_api(self, coin, date_from, date_to, expected):
        actual = tradesapi(moeda=coin)._get_endpoint(date_from = date_from, date_to = date_to)
        assert actual == expected
        
    #Vamos criar um teste para dar uma mensagem de erro quando o date_from for maior que o date_to
    def test_get_endpoint_date_from_greater_than_date_to(self):
        with pytest.raises (RuntimeError): #testando se um erro vai ser erguido
            tradesapi(moeda="TEST")._get_endpoint(
                date_from=datetime.datetime(2023,1,10), 
                date_to=datetime.datetime(2023,1,9)
        )
    # Criado um teste para nossa função _get_unix_epoch que vem antes da TradesApi no nosso arquivo de APIS
    @pytest.mark.parametrize(
        "date, expected",
        [
            (datetime.datetime(2023, 1, 10), 1673319600),
            (datetime.datetime(2023, 1, 9), 1673233200),
            (datetime.datetime(2023, 1, 8), 1673146800),
            (datetime.datetime(2023, 1, 8, 0 ,0, 5), 1673146805),
            (datetime.datetime(2023, 1, 7), 1673060400)
        ]
    )
    def test_get_unix_epoch(self, date, expected):
        actual = tradesapi(moeda="TEST")._get_unix_epoch(date)
        assert actual == expected



# Como a classe mercado bitcoin é abstrata, vamos precisar criar o patch para retornar um set vazio
@pytest.fixture
@patch("apis.mercadobitcoin.__abstractmethods__", set()) 
def fixture_mercadobitcoin():  
    return mercadobitcoin(
            moeda="test"
        )

#Para testar um metodo que recebe informações de fora precisamos utilizar monkey patches:
# Monkey patches é voce sobrescrever a classe no momento da execução do teste com os metodos que voce queira
#*args serie de argumentos posicionais // **kwargs serie de argumentos com chaves
def mocked_requests_get(*args, **kwargs):
    #mockando a resposta
    class MockResponse(requests.Response):
        def __init__(self, json_data, status_code):
            super().__init__()
            self.json_data = json_data
            self.status_code = status_code
            
        #Mockando o metodo json
        def json(self):
            return self.json_data
        
        #se receber uma resposta que não seja 200 aparecer uma mensagem de erro
        def raise_for_status(self) -> None:
            if self.status_code != 200:
                raise Exception
            
     # args[0] = primeiro argumento   
     #se meu primeiro argunto for um endpoint valido quero iniciar a classe mockresponse com o json date com o dict que colocamos no teste
    if args[0] == "valid_endpoint":
        return MockResponse(json_data={"foo": "bar"}, status_code=200)
    else:
        return MockResponse(json_data=None, status_code=404)

# Testando se eu estou chamando o request.get primeiramente
class TestMercadoBitcoinApi:
    # Patch para sobrescrever o metodo requests.get 
    #side_effect = quando o metodo for executado chamar a função mocked_requests_get
    @patch("requests.get") 
    # Patch para sobrescrever o metodo get endpoint
    @patch("apis.mercadobitcoin._get_endpoint", return_value="valid_endpoint")
    def test_get_data_requests_is_called(self, mock_get_endpoint, mock_requests, fixture_mercadobitcoin):
        fixture_mercadobitcoin.get_data()
        #vericar se o request está sendo chamado uma vez com o valor do endpoint
        mock_requests.assert_called_once_with("valid_endpoint")
        
    @patch("requests.get", side_effect=mocked_requests_get)     
    @patch("apis.mercadobitcoin._get_endpoint", return_value="valid_endpoint")
    def test_get_data_with_valid_endpoint(self, mock_get_endpoint, mock_requests, fixture_mercadobitcoin):
        actual = fixture_mercadobitcoin.get_data()
        excepted = {"foo": "bar"}
        assert actual == excepted
    
    #Testar raise for status, se receber uma resposta que não seja 200 aparecer uma mensagem de erro
    @patch("requests.get", side_effect=mocked_requests_get)     
    @patch("apis.mercadobitcoin._get_endpoint", return_value="invalid_endpoint")
    def test_get_data_with_valid_endpoint(self, mock_get_endpoint, mock_requests, fixture_mercadobitcoin):
        with pytest.raises(Exception):
            fixture_mercadobitcoin.get_data()

        
    
        