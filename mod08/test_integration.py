# Teste Blackbox

from mercado_bitcoin.apis import DaySummaryAPI
import datetime

class TestDaySummaryAPI:
    def test_get_data(self):
        actual = DaySummaryAPI(moeda="BTC").get_data(date=datetime.date(2021, 1, 1))
        excepted = {'date': '2021-01-01', 'opening': 152700.00002, 'closing': 153458.29999999, 'lowest': 151539, 'highest': 153975, 'volume': '12583384.54790148', 'quantity': '82.27265844', 'amount': 4824, 'avg_price': 152947.34346135}
        assert actual == excepted
        
    def test_get_data_better(self):
        actual = DaySummaryAPI(moeda="BTC").get_data(date=datetime.date(2021, 1, 1)).get("date")
        excepted = "2021-01-01"
        assert actual == excepted