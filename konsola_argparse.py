import argparse  # => https://docs.python.org/3/library/argparse.html


def parse_args_1():
    parser = argparse.ArgumentParser()
    parser.add_argument('name')  # argument pozycyjny
    parser.add_argument('value', type=int)
    parser.add_argument('--value_2', type=int, required=False, default=-1)  # dla argumentów nazwanych możemy określać, czy są obowiązkowe, czy nie
    # parser.add_argument('value_2', type= int, required=False, default=-1)  # niepoprawne, argumenty pozycyjne nie mogą mieć parametru required - one są zawsze obowiązkowe

    args = parser.parse_args()
    return args


def parse_args_2():
    parser = argparse.ArgumentParser()
    # opis argumentów => https://docs.python.org/3/library/argparse.html#the-add-argument-method
    # metavar = nazwa argumentu w help
    # nargs = liczba argumentów jaka ma być parsowana
    # help = tekst w pomocy dla tego argumentu
    # type = typ danych argumentu
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='liczba/liczby, które będą obsługiwane przez funkcję')

    # dest = nazwa atrybutu, która trzymać wartość tego argumentu w obiekcie zwracanym przez parse_args
    # action = prosta akcja, która ma być wykonana kiedy dany argument ma przypisaną wartość
    #   możliwe akcje => https://docs.python.org/3/library/argparse.html#action

    from functools import reduce
    # funkcja anonimowa przechowywana w zmiennej product bierze na wejście listę
    # której elementy są następnie przez siebie przemnażane
    product = lambda x: reduce(lambda y, z: y*z, x)

    parser.add_argument('--sum', dest='accumulate_fun', action='store_const',
                        const=sum, default=product,
                        help='jeżeli ta flaga jest użyta, wówczas wszystkie liczby zostaną zsumowane, domyślnie - zostaną przez siebie przemnożone.')

    parser.add_argument('--debug', dest='DEBUG', action='store_true', default=False,
                        help='jeżeli podana, wskazuje, że program ma działać w trybie DEBUG')

    args = parser.parse_args()
    # używając funkcji przechowywanej w zmiennej args.accumulate_fun wykonaj operacje na liczbach podanych
    # w zmiennej args.integers i wyświetl jej wynik
    print(args.accumulate_fun(args.integers))

    return args


def main(args):
    print(args)

if __name__ == "__main__":
    # args = parse_args_1()
    args = parse_args_2()
    main(args)
