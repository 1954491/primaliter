#!/usr/bin/env python3

"""
Programme multi-processus pour déterminer si un nombre est premier

2020, Xavier Gagnon
"""
from typing import NoReturn, List
from timeit import default_timer as timer
import math
import sys
import colorama
from multiprocessing import Process
from colorama import Fore

colorama.init()


def main(argv: List[str]) -> None:
    """Fonction principale"""
    debut = timer()

    try:

        if len(argv) == 1:
            raise IndexError("La commande doit avoir au moins un argument")
        nombre = int(argv[1])
        reponse = "Non"
        if nombre <= 100 or nombre % 2 == 0:
            if est_premier_seq(nombre):
                reponse = "Oui"
        else:
            racine = math.isqrt(nombre)

            processus = [Process(target=est_premier_mp, args=(range(3, racine+1, 8), nombre,)),
                         Process(target=est_premier_mp, args=(range(5, racine+1, 8), nombre,)),
                         Process(target=est_premier_mp, args=(range(7, racine+1, 8), nombre,)),
                         Process(target=est_premier_mp, args=(range(9, racine+1, 8), nombre,))]

            nombre_debut = 3
            for ps in processus:
                ps.start()
                print(f"* pid {ps.pid} -- range({nombre_debut}, {racine + 1}, 8)")
                nombre_debut = nombre_debut + 2
            for ps in processus:
                ps.join()

            for ps in processus:
                if ps.exitcode:
                    reponse = "Oui"
                else:
                    reponse = "Non"
                    break

        print(Fore.CYAN + "Selon Xavier Gagn.on:", Fore.RESET, reponse)
        print(Fore.MAGENTA + "Duréé:", timer() - debut, "sec")
    except KeyboardInterrupt:
        duree = timer() - debut
        exexit(KeyboardInterrupt("Interruption clavier"), autre_message=Fore.MAGENTA + f"Duréé: {duree} sec")

    except BaseException as ex:
        exexit(ex)


def est_premier_mp(nombres, nombre: int) -> None:
    """Détérmine si un nombre est premier ou non"""
    """setproctitle(f"XG {nombres}")"""
    try:
        for n in nombres:
            if nombre % n == 0:
                exit(0)

        exit(1)
    except KeyboardInterrupt:
        pass


def est_premier_seq(nombre: int) -> bool:
    """Détermine si un nombre est premier ou non"""
    if nombre < 1:
        raise ValueError("Le nombre doit être > 0")

    if nombre == 1:
        return False

    if nombre <= 3:
        return True

    if nombre % 2 == 0:
        return False

    racine = math.isqrt(nombre)

    for n in range(3, racine + 1, 2):

        if nombre % n == 0:
            return False

    return True


def exexit(ex: BaseException, exit_code: int = 1, autre_message: str = None) -> NoReturn:
    """Rapporte une erreur et termine le programme"""
    print(Fore.YELLOW, "[XG] ",
          Fore.RED, ex.__class__.__name__,
          Fore.YELLOW, ": ", ex,
          file=sys.stderr, sep='')
    if autre_message is not None:
        print(autre_message)
    sys.exit(exit_code)


if __name__ == '__main__':
    main(sys.argv)
