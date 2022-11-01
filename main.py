import time
from random import choices, random, randint
from typing import List, Tuple

from bruteforce import main_brute
from fileReader import read_from_file, Predmet

Kromosom = List[int]
Populacija = List[Kromosom]
lista_predmeta = read_from_file()


# funkcija kreira Kromosom sa rand popunjenim mjestima -> 1 znaci da je predmet u torbi, 0 da nije
def kreiraj_kromosom(duzina: int) -> Kromosom:
    return choices([0, 1], k=duzina)


# funkcija kreira Populaciju zadane velicine
def kreiraj_populaciju(velicina: int, duzina_kromosoma: int) -> Populacija:
    temp = []
    for i in range(velicina):
        temp.append(kreiraj_kromosom(duzina_kromosoma))

    return temp


# fitness funkcija koji vraća ukupnu vrijednost kromosoma
# provjerava je li predmet u torbi (ako je 1 u kromosomu), ako je zbraja masu i vrijednost
# ako sum_masa prijede max_dopustena_masa vraća 0 (odbacuje riješenje) inace vraca sum_vrijednost
def fitness_funkcija(predmeti: [Predmet], max_dopustena_masa: int, kromosom: Kromosom) -> int:
    sum_vrijednost = 0
    sum_masa = 0
    for i, predmet in enumerate(predmeti):
        if kromosom[i] == 1:
            sum_vrijednost += predmet.vrijednost
            sum_masa += predmet.masa
            if sum_masa > max_dopustena_masa:
                return 0

    return sum_vrijednost


# selektira 2 kromosoma iz populacije, Roulette Wheel pristup, jedinke sa vecom vrijednoscu imaju vece
# sanse biti izabrane
def funkcija_selekcije(populacija: Populacija, predmeti: [Predmet], max_dopustena_masa: int) -> Populacija:
    temp = []
    for kromosom in populacija:
        temp.append(fitness_funkcija(predmeti, max_dopustena_masa, kromosom))
    if sum(temp) > 0:
        return choices(population=populacija, weights=temp, k=2)
    else:
        return choices(population=populacija, k=2)


# Ovisno o omjer_rekomb, ili nasumiucno generira tocka_rekom i radi rekombinaciju oko te tocke i vraća dobivene potomke
# ili samo vraća
def funkcija_rekombinacije(k1: Kromosom, k2: Kromosom, omjer_rekomb: float) -> Tuple[Kromosom, Kromosom]:
    if random() < omjer_rekomb:
        duzina = len(k1)
        tocka_rekom = randint(1, duzina - 1)
        return k1[0:tocka_rekom] + k2[tocka_rekom:], k2[0:tocka_rekom] + k1[tocka_rekom:]
    else:
        return k1, k2


def funkcija_mutacije(kromosom: Kromosom, sansa_mutacije: float) -> Kromosom:
    for i, gen in enumerate(kromosom):
        if random() <= sansa_mutacije:
            kromosom[i] = abs(gen - 1)

    return kromosom


def funkcija_main(velicina_populacije: int,
                  duzina_kromosoma: int,
                  lista_pred: [Predmet],
                  masa_ruksaka: int,
                  omjer_rekombinacije: float,
                  sansa_mutacije: float,
                  max_br_generacija: int,
                  elitizam: bool,
                  max_fitness: int
                  ):
    populacija = kreiraj_populaciju(velicina_populacije, duzina_kromosoma)

    for generacija in range(max_br_generacija):
        populacija = sorted(populacija, key=lambda kromosom: fitness_funkcija(lista_pred, masa_ruksaka, kromosom),
                            reverse=True)

        if len(populacija) > 0:
            temp = fitness_funkcija(lista_pred, masa_ruksaka, populacija[0])
            if temp >= max_fitness:
                break

        if elitizam:
            nova_generacija = populacija[0:2]
            for i in range(int((len(populacija) / 2) - 1)):
                roditelji = funkcija_selekcije(populacija, lista_pred, masa_ruksaka)
                potomci = funkcija_rekombinacije(roditelji[0], roditelji[1], omjer_rekombinacije)
                potomak1 = potomci[0]
                potomak2 = potomci[1]
                potomak1 = funkcija_mutacije(potomak1, sansa_mutacije)
                potomak2 = funkcija_mutacije(potomak2, sansa_mutacije)
                nova_generacija += [potomak1, potomak2]
        else:
            nova_generacija = []
            for i in range(int((len(populacija) / 2))):
                roditelji = funkcija_selekcije(populacija, lista_pred, masa_ruksaka)
                potomci = funkcija_rekombinacije(roditelji[0], roditelji[1], omjer_rekombinacije)
                potomak1 = potomci[0]
                potomak2 = potomci[1]
                potomak1 = funkcija_mutacije(potomak1, sansa_mutacije)
                potomak2 = funkcija_mutacije(potomak2, sansa_mutacije)
                nova_generacija += [potomak1, potomak2]

        populacija = nova_generacija

    return populacija, generacija


def ispis_rijesenja(kromosom: Kromosom, predmeti: [Predmet], max_generacije: int, br_generacija: int, max_masa: int):
    print("______________________________________________________GENETSKI_ALGORITAM____________________________________"
          "__________________")
    temp = fitness_funkcija(predmeti, max_masa, kromosom)
    print(f"Ukupna dobit: {temp}")
    print(f"Broji potrebnih generacija: {br_generacija}")
    print(f"Kromosom u genetskom oblliku: {kromosom}")
    print("Predmeti u ruksaku:")
    if br_generacija < max_generacije:
        for i, k in enumerate(kromosom):
            if k == 1:
                print(predmeti[i].ime)
    else:
        print("Nedovoljno generacija!")
    print("____________________________________________________________________________________________________________"
          "__________________")

def main(podrzana_masa:int):
    velicina_pop = int(input("Unesite zeljenu velicinu populacije (int) >>> "))
    rekombinacija = float(input("Unesite omjer rekombinacije u decimalnome obliku (float izedu 0 i 1) >>> "))
    mutacija = float(input("Unesite postotak mutacije u decimalnome obliku (float izedu 0 i 1) >>> "))
    max_br_generacija = int(input("Unesite maksimalan broj generacija (int) >>> "))
    max_fitness = int(input("Unesite maksimalnu vrijednost fitness funkcije (int) >>> "))
    elitizam = input("Zelite li da program koristi elitizam (unesite y/n) >>> ")
    if elitizam == 'y':
        elitizam = True
    else:
        elitizam = False

    start_time = time.time()
    a, b = funkcija_main((velicina_pop), len(lista_predmeta), lista_predmeta, podrzana_masa, rekombinacija, mutacija,
                         max_br_generacija, elitizam, max_fitness)
    stop_time = time.time()

    ispis_rijesenja(a[0], lista_predmeta, max_br_generacija, b, podrzana_masa)
    print(f"Vrijeme za izracun: {stop_time-start_time}s")

podrzana_masa = int(input("Unesite zeljenu masu koju ruksak moze nositi (int) >>> "))
main_brute(podrzana_masa)
main(podrzana_masa)

