import datetime
from abc import ABC, abstractmethod
from typing import List

from apis import DaySummaryAPI

class DataIngestor(ABC):
    def __init__(self, writer, coins: List[str], defaultstartdate: datetime.date) -> None:
        self.defaultstartdate = defaultstartdate
        self.coins = coins
        self.writer = writer
        self._checkpoint = self._load_checkpoint()

    @property
    def _checkpoint_filename(self) -> str:
        return f"{self.__class__.__name__}.checkpoint"

    def _write_checkpoint(self):
        with open(self._checkpoint_filename, "w") as f:
            f.write(f"{self._checkpoint}")

    def _load_checkpoint(self) -> datetime.date:
        try:
            with open(self._checkpoint_filename, "r") as f:
                return datetime.datetime.strptime(f.read(), "%Y-%m-%d").date()
        except FileNotFoundError:
            return self.defaultstartdate

    def _update_checkpoint(self, value):
        self._checkpoint = value
        self._write_checkpoint()
        
    @abstractmethod
    def ingest(self) -> None:
        pass

class DaySummaryIngestor(DataIngestor):

    def ingest(self) -> None:
        #Para dectetar a data de onde eu quero começar
        date = self._load_checkpoint()
        hoje = datetime.date.today()
        if date < hoje:
            for coin in self.coins:
                api = DaySummaryAPI(moeda=coin)
                data = api.get_data(date=date)
                self.writer(coin=coin, api=api.type).write(data)
            self._update_checkpoint(date + datetime.timedelta(days=1)) # para pegar a data atual e somar mais 1 dia