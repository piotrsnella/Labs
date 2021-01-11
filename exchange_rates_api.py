# exchangeratesapi
# https://exchangeratesapi.io/

from pydantic import BaseModel  # https://pydantic-docs.helpmanual.io/
from datetime import datetime
from datetime import date
from typing import List, Dict  # https://docs.python.org/3/library/typing.html
import requests  # https://requests.readthedocs.io/en/master/user/quickstart
import logging

BASE_URL = "https://api.exchangeratesapi.io/latest"


class CurrencyRequest(BaseModel):
    '''
    Klasa przechowująca pierwotne zapytanie.
    '''
    base: str = "EUR"
    symbols: List[str]
    start_at: date = None
    end_at: date = None

    def __str__(self):
        return """
        Dates range: {start:%Y-%m-%d} - {end}
        Base currency: {base}
        Different currencies: {curr}
        """.format(
            start=self.start_at if self.start_at is not None else date.today,
            end=self.end_at.strftime("%Y-%m-%d") if self.end_at is not None else self.end_at,
            base=self.base,
            curr=self.symbols
        )

class CurrencyResponse(BaseModel):
    '''
    Klasa przechowująca pierwotne zapytanie wraz z odpowiedzią serwera.
    '''
    request: CurrencyRequest
    rates: Dict[str, float]
    base: str
    date: date

    def __str__(self):
        return f"""
        Request: {self.request}
        Response:
            date: {self.date}
            base currency: {self.base}
            rates: {self.rates}
        """


def get_currency_rate_mock(request: CurrencyRequest) -> CurrencyResponse:
    response = {
        "base": "EUR",
        "date": "2020-04-23",
        "rates": {
            "USD": 1.0722,
            "PLN": 4.5379
        }
    }
    # TODO: na podstawie zmiennej request oraz response stwórz obiekt CurrencyReponse
    # przypisując go do zmiennej result
    result = None
    return result


def get_currency_rate(request: CurrencyRequest) -> CurrencyResponse:
    response = requests.get(BASE_URL, params=request.dict())
    logging.info(response.request.url)
    # TODO: na podstawie dokumentacji modułu requests - https://2.python-requests.org/en/master/
    # sprawdź jak wyciągnąć odpowiedź serwera w postaci json (w pythonie i tak powinien to będzie słownik)
    # a następnie zapisz go do zmiennej response_json
    response_json = None
    # następnie na podstawie zmiennej request oraz response_json
    # stwórz zmienną response_value, ktora posłuży do stworzenia obiektu typu CurrencyResponse
    # i zwróć go jak wynik działąnia tej funkcji
    result = None
    return result


if __name__=="__main__":
    request_data = {
        "base": "USD",
        "symbols": ["GBP", "PLN"],
        "start_at": datetime(2020, 3, 14),
        "end_at": datetime(2020, 3, 16)
    }

    # test prawdziwego serwera
    # response = get_currency_rate(CurrencyRequest(**request_data))
    # test nieprawdziwego serwera - mock
    response = get_currency_rate_mock(CurrencyRequest(**request_data))
    print(response)
