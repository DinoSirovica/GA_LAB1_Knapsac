import csv
from collections import namedtuple

Predmet = namedtuple("Predmet", ["ime", "vrijednost", "masa"])


def read_from_file():
    temp_lista = []
    with open('inputList.csv', newline='\n') as f:
        reader = csv.reader(f)
        for row in reader:
            ime = row[0]
            vrijednost = row[1]
            masa = row[2]
            temp_lista.append(Predmet(ime, int(vrijednost), int(masa)))
            temp_lista.append(Predmet(ime, int(vrijednost), int(masa)))
            temp_lista.append(Predmet(ime, int(vrijednost), int(masa)))

    return temp_lista