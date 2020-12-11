#!/usr/bin/env python3

"""
Programme séquentiel pour déterminer si un nombre est premier

2020, Xavier Gagnon
"""
from typing import NoReturn
from timeit import default_timer as timer
import math
import sys
import colorama
from colorama import Fore

colorama.init()


def main() -> None:
    """Fonction principale"""
    debut = timer()
    try:

        if len(sys.argv) == 1:
            raise IndexError("La commande doit avoir au moins un argument")

        reponse = "Non"
        if est_premier_seq(int(sys.argv[1])):
            reponse = "Oui"

        print(Fore.CYAN + "Selon Xavier Gagnon:", Fore.RESET, reponse)
        print(Fore.MAGENTA + "Duréé:", timer() - debut, "sec")
    except KeyboardInterrupt:
        print(Fore.MAGENTA + "Duréé:", timer() - debut, "sec")
        exexit(KeyboardInterrupt("Interruption clavier"))

    except BaseException as ex:
        exexit(ex)


def est_premier_seq(nombre: int) -> bool:
    """Détermine si un nombre est premier ou non"""
    if nombre < 1:
        raise ValueError("Le nombre doit être positif")

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


def exexit(ex: BaseException, exit_code: int = 1) -> NoReturn:
    """Rapporte une erreur et termine le programme"""
    print(Fore.YELLOW, "[XG] ",
          Fore.RED, ex.__class__.__name__,
          Fore.YELLOW, ": ", ex,
          file=sys.stderr, sep='')
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
