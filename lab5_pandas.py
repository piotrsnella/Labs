#!/usr/bin/env python
# coding: utf-8

# # Python w analizie ekonomicznej - poziom zaawansowany, warsztaty
# ## Temat: Pandas - wstęp.
# 
# (odpowiedzi do zadań w czasie prezentacji proszę udzielać na czacie)
# 
# Jakub Tomczak *jakub.tomczak@cdv.pl*

# Agenda:
# 
#     * wstęp do biblioteki Pandas

# [Pandas](https://pandas.pydata.org/pandas-docs/stable/index.html) - open source'owa (kod jest dostępny online) biblioteka dostarczająca wysokiej wydajności oraz łatwe w użyciu struktury danych oraz narzędzia do analizy danych w języku python.

# ### Instalacja modułu `pandas`
# 
# Otwieramy konsolę `Anaconda prompt`.
# <img src='imgs/anaconda_prompt.png' width="500" />

# oraz instalujemy pandas za pomocą komendy
# ```bash
#     pip install pandas --user
# ```
# 
# w przypadku Anacondy powinien być już zainstalowany.
# 
# Przechodzimy do folderu z plikiem `lab5_pandas.ipynb` w konsoli (za pomocą komendy `cd /d folder_z_plikiem_lab5_pandas.ipynb`).
# W konsoli wpisujemy `jupyter notebook` - powinna otworzyć się przeglądarka internetowa wraz z wyświetloną listą pliku z folderu w którym byliśmy podczas uruchamiania komendy.
# Otwieramy plik `lab5_pandas.ipynb`.
# <img src="imgs/anaconda_jupyter notebook.png" width=600 />

# <img src="imgs/anaconda_jupyter notebook1.png" width=800 />

# Moduł `Pandas` będziemy importowali zawsze poprzez komendę

# In[2]:


import pandas as pd


# wówczas wszystkie funkcje dostępne w module `pandas` będziemy wywoływali poprzez kod `pd.[nazwa funkcji]`.

# ## Wczytywanie danych
# 
# Pandas obsługuje wiele znanych formatów plików takich jak `csv`, `hdf5`, `json`, `html`, binarne, `sql`, `python pickle`, `SAS` ...
# Na dzisiejszych zajęciach zajmiemy się plikami `csv` . W archiwum z plikami do tych zajęć znajduje się folder `files`, a w nim plik `cars.csv`.
# To ten sam plik, który jest w przykładowych zbiorach do projektu.
# ```python
# dataset = pd.read_csv('files/cars.csv', sep=';')
# ```

# In[52]:


dataset = pd.read_csv('files/cars.csv', sep=';')


# Wyświetlmy wczytany zbiór danych. Zauważmy, że oprócz kolumny `id`, przed nią, znajdują się indeksy wierszy - to indeksowanie jest automatycznie dodane przez pandas.

# In[9]:


dataset


# pandas wczytując dane tworzy obiekt `DataFrame`, który przechowuje kolumny z danymi jako typ `Series`.

# In[15]:


print('Typ wczytanych danych', type(dataset))
print('Typ kolumny id', type(dataset['id']))


# Wszystkie dane zostały poprawnie wczytane. 
# Pandas potrafi samemu na podstawie danych w kolumnach ustawić odpowiedni typ danych w danej kolumnie - zgaduje, należy więc sprawdzić jakie typy przypisał wczytanym kolumnom.
# Sprawdźmy jakie są typy kolumn za pomocą funkcji `info`, którą wywołujemy na zbiorze danych.

# In[16]:


dataset.info()


# Widzimy, że pandas potrafi również podliczyć liczbę pustych wartości już na etapie wczytywania danych - kolumna `Non-Null Count` dla wiersza `model`, gdzie mamy liczbę 11 co oznacza, że są 3 puste wartości (mają typ Null).

# ## Wyświetlanie danych z ramki danych `DataFrame`
# 
# Chcąc wyświetlić tylko część danych z ramki możemy skorzystać z kilku metod. Niestety nie możemy użyć indeksowania jak w zwykłej liście.

# In[21]:


dataset[0]


# Aby wyświetlić pierwszy wiersz możemy użyć metody `iloc`, która pozwala na wybieranie wierszy oraz kolumn z ramki danych.

# In[23]:


# wybranie całego pierwszego wiersza, : oznacza wybranie wszystkich kolumn - podobnie jak w numpy
dataset.iloc[0, :]


# In[33]:


print('wybranie całego pierwszego wiersza, a z niego tylko kolumn `marka` oraz `cena`')
print(dataset.iloc[0, [1, 5]])
print()
print('niestety nie możemy używać nazw kolumn korzystając z iloc')
dataset.iloc[0, ['marka', 'cena']]


# Możemy natomiast wybrać zakres wierszy oraz zakres kolumn korzystając z podobnej metody jak w przypadku macierzy w `numpy`, czy list pythonowych.

# In[35]:


# wyświetl co drugi wiersz od 3 do 8 (wyłącznie) a z nich weź tylko kolumny od 2-giej do 4 (wyłącznie)
dataset.iloc[2:8:2, 1:3]


# Inną metodą do wyświetlania tylko wycinka danych jest metoda `loc`, bazuje ona jednak na indeksach dodanych przez pandas. W przypadku, gdy indeksy są po kolei nie ma różnicy między metodą `iloc` a `loc`, natomiast różnice pojawiają się, gdy usuniemy część danych.
# 

# In[58]:


dataset_removed = dataset.drop(2)
dataset_removed


# In[54]:


# usuwamy 3 wiersz
dataset_removed.loc[2]


# In[56]:


# usuwamy 3 wiersz
dataset_removed.iloc[2]


# Dlatego też należy o tym pamiętać. Problem ten można obejść jeżeli tworzymy indeks danej ramki danych po każdym usunięciu danych za pomocą metody [reset_index](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.reset_index.html#pandas.DataFrame.reset_index)

# In[109]:


dataset_removed.reset_index(drop=True, inplace=True)
dataset_removed.loc[2]


# Jeżeli chcemy wyciągać tylko kolumny z ramki danych możemy to zrobić z wykorzystaniem indeksowania ramki danych

# In[112]:


dataset[['cena', 'marka']]


# Albo podając nazwę kolumny bezpośrednio (uwaga, metoda tylko dla kolumn które mają poprawną nazwę jeżeli chodzi o nazewnictwo zmiennych w python). Metoda ta służy do wyciągania tylko 1 kolumny na raz.

# In[113]:


dataset.cena


# Wyświetlamy, przy użyciu metody `info` po raz kolejny typy danych w ramce - tym razem sprawdzamy jakie typy danych zostały przypisane kolumnom.

# In[59]:


dataset.info()


# Jak widać `id` zostało poprawnie zidentyfikowane jako liczba, `marka`, `model` oraz `typ samochodu` są ciągami znaków, więc będą miały typ `object`.
# Rocznik został również rzutowany na poprawny typ danych - liczba całkowita.
# Natomiast cena nie jest poprawnie ustawiona - jest typu `object`.
# Stało się tak dlatego, że w cenie występują spacje. Aby ustawić poprawny typ danych musimy więc usunąć spacje i spróbować rzutować dane na typ liczbowy ponownie.

# Aby usunąć spacje z ciągu znaków i rzutować ten ciąg znaków na liczbę wykorzystamy następujący sposób

# In[68]:


x = '40 000'
def string_with_space_to_int(x):
    return int(x.replace(' ', ''))

x_int = string_with_space_to_int(x)
print(x_int)
print(type(x_int))


# Pobieramy dane z kolumny `cena` do zmiennej `price_column`:

# In[62]:


price_column = dataset['cena']
price_column


# W zmiennej `price_column` przechowujemy dane z kolumny `cena`. Zmienna `price_column` jest typu `Series`

# In[63]:


type(price_column)


# Możemy na niej wywołać metodę `map` - aplikuje ona podaną funkcję (może być to funkcja anonimowa lambda) do każdego elementu w serii

# In[71]:


price_column_int = price_column.map(string_with_space_to_int)


# Jak widzimy w zmiennej `price_column_int` są już dane liczbowe, zamieniamy wartości w kolumnie z ceną w naszej oryginalnej ramce danych na ceny, które są w formacie liczbowym:

# In[74]:


dataset['cena'] = price_column_int
dataset


# In[75]:


dataset.info()


# Teraz zajmujemy się datami. One też są w niepoprawnym formacie. Chcielibyśmy, aby miał format daty - wówczas łatwo będzie sprawdzić, która data jest pierwsza lub pobrać rekordy w podanym przedziale dat. W tym celu ponownie wyciągamy całą kolumnę do zmiennej:

# In[76]:


date_column = dataset['data i godzina dodania ogłoszenia']
date_column


# W tym przypadku nie musimy korzystać z metody `map` - pandas ma już przygotowaną metodę [pd.to_datetime](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html) . Jako jej argumenty należy podać ramkę danych/serię danych oraz format danych, które są datami (pandas musi wiedzieć jaki jest format ciągu znaków zapisany w danych, tak żeby poprawnie zidentyfikować dzień, miesiąc, rok, godzinę, czy miuntę). Jak poprawnie ustawić format danych możemy przeczytać [tutaj](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior).
# 
# W naszym przypadku dane są w formacie `dzień-miesiąc-rok godzina:minuta`, co odpowiada formatowi `dd-mm-YYYY hh:MM`.

# In[90]:


date_column_as_datetime = pd.to_datetime(date_column, format='%d-%m-%Y %H:%M')
date_column_as_datetime


# następnie przypisujemy daty do oryginalnej ramki danych

# In[91]:


dataset['data i godzina dodania ogłoszenia'] = date_column_as_datetime


# In[92]:


dataset.info()


# ### Statystyki dla kolumn
# 
# Obliczanie statystyk dla kolumn z użyciem pandas jest wyjątkowo proste. Najczęściej jedyne co musimy wykonać to wywołać odpowiednią metodę na kolumnie z danymi.
# Dla przykładu, obliczenie minimalnej wartości dla kolumny cena możemy wykonać za pomocą wyrażenia:
# 

# In[94]:


dataset.loc[:, ['cena']].min()


# Albo jeszcze prościej

# In[96]:


print(dataset.cena.min())
print(dataset['cena'].min())


# Podobnie wywołujemy metody obliczające wartość maksymalną

# In[97]:


dataset.cena.max()


# Średnią

# In[98]:


dataset.cena.mean()


# Odchylenie standardowe

# In[99]:


dataset.cena.std()


# Natomiast dla każdej z kolumn możemy wywołać metodę `describe()`, która, na podstawie typu danych danej kolumny, wypisze podsumowanie danej kolumny

# In[102]:


dataset.cena.describe()


# In[103]:


dataset.model.describe()


# In[104]:


dataset['data i godzina dodania ogłoszenia'].describe()

