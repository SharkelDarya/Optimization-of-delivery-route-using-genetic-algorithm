# Optimization-of-delivery-route-using-genetic-algorithm
System znajdowania najbardziej optymalnej ścieżki pomiędzy dziesięcioma miastami przy użyciu algorytmu genetycznego.
<p align="left">
   <img src="https://img.shields.io/badge/Engine-VS%20Code-2B7FB8" alt="Engine">
  <img src="https://img.shields.io/badge/Version-1.86-39A8F2" alt="Version Engine">
</p>

## About

Projekt rozwiązuje problem optymalizacji trasy dla podróżującego sprzedawcy przy użyciu algorytmu genetycznego. Dane wejściowe obejmują macierz odległości między różnymi miastami w Polsce, a także koszty paliwa i średnią prędkość podróży. System oblicza najlepszą ścieżkę i przedstawia ją jako stronę html.

## Documentation

### Libraries
**-** **`pandas`**, **`random`**, **`geopy`**, **`folium`**

### Definicja danych
- Macierzy odległości pomiędzy miastami, kosztów paliwa i jego ilość.
  
### Generowanie genotypu
- Tworzy losową trasę w postaci np. {1, 5, 3, 6, 7, 2, 4, 8, 10, 9}.
  
### Inicjalizacja populacji
- Tworzenie początkowej populacji o rozmiarze zmiennej POPULATION_SIZE.
  
### Ocena funkcji docelowej
-  Obliczenie efektywności trasy według odległości, kosztu i ilości paliwa.
  
### Ewolucja populacji
- Tworzenie algorytmu genetycznego zaimplementując metody selekcji, krzyżowania i mutacji.
- Ocena każdego osobnika.
  
### Optymalizacja
- Kilka generacji jest przeprowadzanych z ustawieniami algorytmu genetycznego (liczba pokoleń, rozmiar turnieju, prawdopodobieństwo krzyżowania i mutacji).
  
### Wizualizacja wyników
- Wykorzystuje bibliotekę Folium do stworzenia interaktywnej mapy pokazującej miasta i optymalną trasę.
  
## Developers

- Darya Sharkel (https://github.com/SharkelDarya)
