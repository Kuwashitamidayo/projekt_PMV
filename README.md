# Projekt PMV
Projekt dotyczący inteligentnych budynków, służący do określania optymalnych nastaw temperatury i wilgotności dla zadanych parametrów dla najwyższego komfortu przebywania danej osoby. Liczenie współczynnika PPV na podstawie danych zewnętrznych (temperatura i wilgotność - mierzone z DHT11) i danych zadanych przez użytownika z użyciem Raspberry Pi.

## Założenia
- liczenie wpółczynników komfortu (PMV), odsetku niezadowolonych (PPD) na podstawie parametrów (temperatura, wilgotność itd.),
- pomiar temperatury i wilgotności z czujnika DHT11 (po niewielkich zmianach w kodzie również na DHT22)
- implementacja na Raspberry Pi
- możliwość wyboru współczynnika ubioru i metabolizmu na bazie gotowców z rozwijanej listy, lub ich ręczne wpisywanie

## Zdjęcie poglądowe

<p align="center">
  <img src="https://github.com/Kuwashitamidayo/projekt_PMV/tree/master/pictures/screenshot_001.png">
</p>

## Wykorzystane biblioteki
- PyQT5 (sudo apt-get install python-pyqt5)
- PySide (sudo apt-get install python-pyside) - póki co nieużywana
- Adafruit_DHT (biblioteka w kodzie)
