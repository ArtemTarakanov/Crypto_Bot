import requests
import json
from config import keys


class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount:str):

        if quote == base:
            raise ConvertionException('Нельзя переводить одинаковые валюты')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException('Не удалось обработать валюту')
        
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException('Не удалось обработать валюту')
        
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('Не удалось обработать количество валюты')
        
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = json.loads(r.content)[keys[base]]

        return total_base