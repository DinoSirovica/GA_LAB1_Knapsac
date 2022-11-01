import time

from fileReader import read_from_file

lista_predmeta = read_from_file()


def bruteforce(predmeti, dopustena_masa: int):
    sum_vrijednosti = 0
    u_ruksaku = []

    if len(predmeti) == 0:
        return 0, []

    for i, pred in enumerate(predmeti):
        # preskoci krug ako je pred.masa > dopustena_masa
        if pred.masa > dopustena_masa:
            continue

        vrijednost, stavljeno = bruteforce(predmeti[i + 1:], dopustena_masa - pred.masa)
        if vrijednost + pred.vrijednost >= sum_vrijednosti:
            sum_vrijednosti = vrijednost + pred.vrijednost
            u_ruksaku = [pred] + stavljeno

    return sum_vrijednosti, u_ruksaku


def main_brute(max_tezina_ruksaka):
    print("______________________________________________________BRUTEFORCE_ALGORITHM__________________________________"
          "____________________\n")
    start_time = time.time()
    a, b = bruteforce(lista_predmeta, max_tezina_ruksaka)
    stop_time = time.time()
    print(f"Vrijeme za izracun: {stop_time - start_time}s")
    print(f"Ukupna dobit: {a}")
    print(b)
    print("\n____________________________________________________________________________________________________________"
          "____________________\n")


