import argparse
from exchange_rates_api import get_currency_rate, get_currency_rate_mock, CurrencyRequest
from datetime import datetime


def parse_args():
    def parse_date(x):
        try:
            return datetime.strptime(x, "%Y-%m-%d").date()
        except Exception as e:
            msg = f"Not a valid date: '{x}'."
            raise argparse.ArgumentTypeError(msg)

    # TODO: dopisz kod, który będzie parsował argumenty za pomocą klasy ArgumentParser
    # dokumentacja klasy https://docs.python.org/3/library/argparse.html
    # argumenty które mają być parsowane to:
    # `base` - argument pozycyjny, typ string
    # `symbols` - argument pozycyjny, typ string, przyjmujący więcej niż jedną wartość (listę), użyj parametru nargs='+'
    # `--start_at` - argument nazwany, domyślnie None, parsowany przez funkcję parse_data, użyj parametru type=parse_data
    # `--end_at` - argument nazwany, domyślnie None, parsowany przez funkcję parse_data, użyj parametru type=parse_data
    # `--release_ver` - argument nazwany, domyślnie False, niewymagany, jeżeli jest podany to powinien przechowywać wartość True -
    #                   użyj parametru action='store_true',
    #                   poza tym powinien zapisywać wartość do zmiennej RELEASE - użyj parametru dest
    parser = argparse.ArgumentParser()
    parser.add_argument('base')
    parser.add_argument('symbols')
    parser.add_argument('--start_at')
    parser.add_argument('--end_at')
    parser.add_argument('--release_ver')

    args = parser.parse_args()
    print(f'Program działa w trybie RELEASE? {args.RELEASE}')
    return args


def print_exchanges_rate(args):
    # TODO: stwórz obiekt CurrencyRequest na podstawie argumentów - zmienna args
    request=None
    # TODO: w zależności od wartości zmiennej args.RELEASE
    # wywołaj funkcję get_currency_rate z argumentem request jeżeli args.RELEASE ma wartość True
    # wywołaj funkcję get_currency_rate_mock z argumentem request jeżeli args.RELEASE ma wartość False
    # i zapisz wartość zwróconą przez funkcje do zmiennej result
    result = None
    print('results:')
    print(result)


if __name__ == "__main__":
    args = parse_args()
    print(args)
    print_exchanges_rate(args)
