import datetime
import json
import os
from typing import List
from apis import DaySummaryAPI, tradesapi
from ingestors import DaySummaryIngestor

class DataTypeNotSupportedForIngestionException(Exception):
    def __init__ (self, data):
        self.data = data
        self.message = f"Data type {type(data)} is not suported for ingestion"
        super().__init__(self.message)

# Inserir dados num arquivo
class DataWriter:
    
    def __init__(self, coin: str, api: str) -> None:
        self.api = api
        self.coin = coin
        now = datetime.datetime.now()
        current_time = now.strftime("%H_%M_%S")
        self.filename = f"{self.api}/{self.coin}/{str(datetime.datetime.now().date()) + current_time}.json"
        
    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, "a") as f:
            f.write(row)

    def write(self, data: [List, dict]):
        #se esse dado for do tipo dict eu quero só gravar, chamando o metodo write row e inserir a linha no arquivo
        #Utilizando o metodo isinstance, que verifica se o dado é uma instacia de alguma clase
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        #se for uma lista = Para cada elemento na lista vai ser um dict
        elif isinstance(data, List):
            for element in data:
                self.write(element)
        else:
            raise DataTypeNotSupportedForIngestionException(data)


