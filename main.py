import pandas as pd
import random
from geopy.geocoders import Nominatim
import folium
from folium import plugins
from geopy.geocoders import Nominatim

NUM_CUSTOMERS = 10
POPULATION_SIZE = 450

#KROK 0
macierzKilometrow = [   #1        2     3       4      5     6      7      8      9      10
                        [0,     426.5, 732.9, 416,   569.8, 753.6, 653,   264,   566,   443],   # 1
                        [426.5, 0,     584.3, 483,   519.6, 429.4, 596.3, 167,   340.5, 340.3], # 2
                        [732.9, 584.3, 0,     522.2, 413.5, 349.8, 333.7, 477,   173.1, 306.4], # 3
                        [416,   483,   522.2, 0,     197.2, 542.8, 272.2, 311,   354.8, 220.8], # 4
                        [569.8, 519.6, 413.5, 197.2, 0,     493.7, 80.9,  412.3, 294.7, 202.7], # 5
                        [753.6, 429.4, 349.8, 542.8, 493.7, 0,     493.7, 497.7, 198.4, 325],   # 6
                        [653,   596.3, 333.7, 272.2, 80.9,  493.7, 0,     488,   293.8, 278.4], # 7 
                        [264,   167,   477,   311,   412.3, 497.7, 488,   0,     303.9, 232.4], # 8
                        [566,   340.5, 173.1, 354.8, 294.7, 198.4, 293.8, 303.9, 0,     136.4], # 9
                        [443,   340.3, 306.4, 220.8, 202.7, 325,   278.4, 232.4, 136.4, 0]      # 10 
                    ]

miasta = ['Szczecin', 'Gdansk', 'Lublin', 'Wroclaw', 'Katowice',
          'Bialystok', 'Krakow', 'Bydgoszcz', 'Warszawa', 'Lodz']

print('Kilometry:')

df = pd.DataFrame(macierzKilometrow, index=miasta, columns=miasta)
pd.set_option('display.max_columns', None)  
pd.set_option('display.max_rows', None)     
pd.set_option('display.width', None)        
print(df)

print()
# Cena paliwa
cena_paliwa = 6

def przelicz_na_koszty(kilometry):
    return round((kilometry / 100) * cena_paliwa * 8)

# koszty paliwa
macierzKosztowPaliwa = [
    [przelicz_na_koszty(km) for km in wiersz] for wiersz in macierzKilometrow]

print('Koszty paliwa:')

df = pd.DataFrame(macierzKosztowPaliwa, index=miasta, columns=miasta)
pd.set_option('display.max_columns', None)  
pd.set_option('display.max_rows', None)     
pd.set_option('display.width', None)        
print(df)

# km/h
srednia_predkosc = 60

def przelicz_na_czas(kilometry):
    return round(kilometry / srednia_predkosc)

# Czasu podróży
macierzCzasowPodrozy = [
    [przelicz_na_czas(km) for km in wiersz] for wiersz in macierzKilometrow
]

print('Czas dojazdu:')

df = pd.DataFrame(macierzCzasowPodrozy, index=miasta, columns=miasta)
pd.set_option('display.max_columns', None)  
pd.set_option('display.max_rows', None)     
pd.set_option('display.width', None)        
print(df)

# Krok 1: Kodowanie genotypu
def generate_individual():
    return random.sample(range(1, NUM_CUSTOMERS + 1), NUM_CUSTOMERS)

genotyp_przyklad = generate_individual()
print("Przykladowy genotyp:", genotyp_przyklad, flush=True)

# Krok 2: Inicjalizacja populacji
def generate_initial_population(population_size):
    return [generate_individual() for _ in range(population_size)]

populacja = generate_initial_population(POPULATION_SIZE)

for individual in populacja:
    print("Przykladowa chromosoma:", individual)

# Krok 3: Ewaluacja funkcji celu

def get_kilometry(index1, index2):
    distance = macierzKilometrow[index1][index2]
    return distance

def get_cena(index1, index2):
    cena = macierzKosztowPaliwa[index1][index2]
    return cena

def get_czas(index1, index2):
    czas = macierzCzasowPodrozy[index1][index2]
    return czas

def sum_kilo(path):
    sum = 0
    for i in range(len(path) - 1):
        index1 = path[i] - 1  
        index2 = path[i + 1] - 1
        kilo = get_kilometry(index1, index2)
        sum += kilo
    return sum

def sum_cena(path):
    sum = 0
    for i in range(len(path) - 1):
        index1 = path[i] - 1  
        index2 = path[i + 1] - 1
        cena = get_cena(index1, index2)
        sum += cena
    return sum

def sum_czas(path):
    sum = 0
    for i in range(len(path) - 1):
        index1 = path[i] - 1  
        index2 = path[i + 1] - 1
        czas = get_czas(index1, index2)
        sum += czas
    return sum

def ocena_osobnika(chromosom):
    print(chromosom)
    
    kilo = sum_kilo(chromosom)
    cena = sum_cena(chromosom)
    czas = sum_czas(chromosom)

    ocena_trasy = (kilo / (cena * czas)) * 100
    return ocena_trasy

przykladowa_populacja = [8, 9, 2, 5, 7, 3, 4, 6, 10, 1]
efektywnosc = ocena_osobnika(przykladowa_populacja)
print(f"Koeficjent efektywnosci: {efektywnosc}")

def turniejowa_selekcja(populacja, rozmiar_turnieju):
    wybrane = []
    for _ in range(len(populacja)):
        turniej = random.sample(populacja, rozmiar_turnieju)
        wybrane.append(max(turniej, key=ocena_osobnika))
    return wybrane

def krzyzowanie_jednopunktowe(rodzic1, rodzic2):
    punkt_krzyzowania = random.randint(1, len(rodzic1) - 1)
    potomek1 = rodzic1[:punkt_krzyzowania] + [gen for gen in rodzic2 if gen not in rodzic1[:punkt_krzyzowania]]
    potomek2 = rodzic2[:punkt_krzyzowania] + [gen for gen in rodzic1 if gen not in rodzic2[:punkt_krzyzowania]]
    return potomek1, potomek2

def mutacja_zmiana_miasta(rodzic):
    indeks1, indeks2 = random.sample(range(len(rodzic)), 2)
    potomek = rodzic.copy()
    potomek[indeks1], potomek[indeks2] = potomek[indeks2], potomek[indeks1]
    return potomek


def algorytm_genetyczny(populacja, liczba_generacji, rozmiar_turnieju, prawdopodobienstwo_krzyzowania, prawdopodobienstwo_mutacji):
    for generacja in range(liczba_generacji):
        # Selekcja
        rodzice = turniejowa_selekcja(populacja, rozmiar_turnieju)
        
        # Krzyżowanie
        nowe_pokolenie = []
        for i in range(0, len(rodzice), 2):
            if random.random() < prawdopodobienstwo_krzyzowania:
                potomek1, potomek2 = krzyzowanie_jednopunktowe(rodzice[i], rodzice[i + 1])
                nowe_pokolenie.extend([potomek1, potomek2])
            else:
                nowe_pokolenie.extend([rodzice[i], rodzice[i + 1]])
        
        # Mutacja
        for i in range(len(nowe_pokolenie)):
            if random.random() < prawdopodobienstwo_mutacji:
                nowe_pokolenie[i] = mutacja_zmiana_miasta(nowe_pokolenie[i])
        
        # Ocena pokolenia
        oceny = [ocena_osobnika(chromosom) for chromosom in nowe_pokolenie]
        
        # Wybór nowej populacji
        populacja = [nowe_pokolenie[i] for i in sorted(range(len(nowe_pokolenie)), key=lambda x: oceny[x], reverse=True)[:POPULATION_SIZE]]
        
        #najlepszy wynik w każdej generacji
        najlepszy_chromosom = populacja[oceny.index(max(oceny))]
        print(f"Generacja {generacja + 1}, Najlepszy chromosom: {najlepszy_chromosom}, Ocena: {max(oceny)}")

    return najlepszy_chromosom

# Ustawienia algorytmu genetycznego
LICZBA_GENERACJI = 7
ROZMIAR_TURNIEJU = 5
PRAWDOPODOBIENSTWO_KRZYZOWANIA = 0.7
PRAWDOPODOBIENSTWO_MUTACJI = 0.2

populacja = algorytm_genetyczny(populacja, LICZBA_GENERACJI, ROZMIAR_TURNIEJU, PRAWDOPODOBIENSTWO_KRZYZOWANIA, PRAWDOPODOBIENSTWO_MUTACJI)
print(populacja)

city_coordinates = {
        1: (53.4289, 14.5530),   # Szczecin
        2: (54.3520, 18.6466),   # Gdansk
        3: (51.2465, 22.5684),   # Lublin
        4: (51.1079, 17.0385),   # Wroclaw
        5: (50.2649, 19.0238),   # Katowice
        6: (53.1325, 23.1688),   # Bialystok
        7: (50.0647, 19.9450),   # Krakow
        8: (53.1235, 18.0076),   # Bydgoszcz
        9: (52.2297, 21.0122),   # Warszawa
        10: (51.7592, 19.4559)   # Lodz
    }

def create_route_map(city_numbers):
    m = folium.Map(location=[53.4289, 14.5530], zoom_start=6)

    for city_num in city_numbers:
        coord = city_coordinates[city_num]
        folium.Marker(coord, popup=f'City {city_num}').add_to(m)

    route_coordinates = [city_coordinates[city_num] for city_num in city_numbers]
    folium.PolyLine(route_coordinates, color="blue", weight=2.5, opacity=1).add_to(m)

    m.save('route_map.html')

create_route_map(populacja)
