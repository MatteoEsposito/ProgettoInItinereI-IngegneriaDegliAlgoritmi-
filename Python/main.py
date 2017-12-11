# coding=utf-8
# main.py
# Autore: Matteo Esposito
# Versione di Python: 2.6.9

import time

from lib.settings import DEBUG, RELEASE
from lib.ProjUtilities import generateRandomAVLTree, concatenate

global A, B

def benchmark(n):
    """
    Main delle funzioni di benchamrking, si occupa di creare gli alebri AVL e di richiamare
    la "doTest" al fine di raccogliere informazioni e dati
    sul tempo di esecuzione dell'algoritmo in relazione alla quantita dell'input
    :param n: numero di volte che si vuole testare l'algoritmo
    :return:
    """
    global A, B
    while n > 0:
        if n % 2 == 0:
            d = 0
        else:
            d = 1
        A, B = generateRandomAVLTree(0, 255*n, 50*n, 10*n, d)
        doTest(n,50*n,10*n,d)
        n = n-1

def doTest(i, elements,diff, dir):
    """
    Funzione usata per fare il benchmarking,
    data la natura del'algoritmo e la richiesta di generare in runtime degli alberi AVL
    ho considerato come scelta "migliore" lo spezzare il codice in due frammenti in cui
    viene semplicemente calcolato il SOLO tempo di esecuzione dell'algoritmo e non
    anche della creazione degli alberi AVL
    :param i: i-esima iterazione
    :param elements: elementi dell'albero più basso
    :param diff: numero di elementi da aggiungrìere in più all'albero più alto rispetto all'albero più basso
    :param dir: 0: A più alto di B
                1: B più alto di A
    :return: None
    """
    global A, B
    tempo_iniziale = time.time()
    concatenate(A,B)
    tempo_finale = time.time()
    d = "direzione"
    if dir == 0:
        d = "B"
    else:
        d = "A"
    eltot = 2*elements + diff
    print "Test N:", str(i), ",", str(tempo_finale - tempo_iniziale), ", secondi,", "elementi: ", str(elements), ", differenza di elementi: ", str(diff), "elementi totali: ", str(eltot), ", albero maggiore: ", d


if __name__ == "__main__":
    # Main Debugging and Testing Unit:
    # Ho scelto di implementare così il mio algoritmo
    # di seguito è possibile cambaire il valore della variabile
    # tra 0 ed 1 con i seguenti risultati:
    # Valori di C:
    #
    # 0: Debug di un generico albero AVL
    # 1: Benchmarking dell'algoritmo
    #

    C = 0     # Modificare questo valore per accedere ai due diversi ambienti di Testing
              # Per Avere una Verbosità maggiore nei risultati aggiustare i realtivi FLAG
              # nel file settings.py nella cartella lib ( di Default essi sono settati su FALSE )

    if C == 0:

        A, B = generateRandomAVLTree(0, 20000, 100, 300, 0)
        C = concatenate(A, B)
        if DEBUG | RELEASE:
             print("\n \n Albero Concatenato \n \n ")
             C.tree.stampa()

    elif C == 1:

        print "######## Inizio Test ########"
        benchmark(1000)
        print "######## Fine Test ########"

    else:

        print "Scelta non valida!"

