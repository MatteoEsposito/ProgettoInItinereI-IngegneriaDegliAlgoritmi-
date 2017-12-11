# coding=utf-8
# ProjUtilities.py
# Autore: Matteo Esposito
# Versione di Python: 2.6.9

import random

from extendedAVL import ExtendedAVL
from settings import DEBUG


def createAVLByArray(array):
    '''
    Classe usata per creare un albero AVL da un Array

    :Time: O(n)
    :param array: Array of integers
    :return: ExtendedAVL - AVL Tree
    '''
    avl = ExtendedAVL()
    for i in range(len(array)):
        avl.insert(i, array[i])

    return avl


def generateAVLBYRandomSeeding(start, end, n):
    """
    Classe usata per generare un singolo Albero AVL da numeri pseudo-randomizzati
    :param start: int - inzio del range dal quale generare i numeri
    :param end: int - fine del range dal quale generare i numeri
    :param n: quantità di numeri da restituire nell'array
    :Time: O(n)
    :return: ExtendedAVL - AVL Tree
    """

    try:
        return createAVLByArray(random.sample(range(start, end), n))
    except ValueError:
        print('Il numero di campioni supera il range specificato')
        exit(1)


def generateRandomAVLTree(start,end,n,diff,maj):
    """
    Classe usata per generare una coppia Albero AVL da numeri pseudo-randomizzati che differiscono per:
    > Una certa quantità diff di elementi
    > Un Albero ha chiavi tutte maggiori del secondo e/o viceversa

    :param start: int - inzio del range dal quale generare i numeri
    :param end: int - fine del range dal quale generare i numeri
    :param n: quantità di numeri da restituire nell'array
    :param diff: quantita di elementi di differenza tra albero più alto e più basso, la differenza viene aggiunta allo
                 albero più alto
    :param maj: 0: A più alto di B;
                1: B più alto di A;
    :Time: O(n)
    :return: Tuple( ExtendedAVL - AVL Tree (A), ExtendedAVL - AVL Tree  (B), )
    """

    if maj==0 :
        A = generateAVLBYRandomSeeding(-end,-start-diff,n + diff)
        B = generateAVLBYRandomSeeding(start,end,n)

    elif maj == 1:
        A = generateAVLBYRandomSeeding(-end, -start, n)
        B = generateAVLBYRandomSeeding(start, end + diff, n + diff)
    else:
        print("GenerateAVLBYRandomSeeding: Valore non accettato!")
        exit(1)
    return A, B


# Main Code per la Concatenazione
def concatenate(A, B):
    """
    Main Core dell'algoritmo del progetto questa classe, estensivamente documentata nella relazione
    presi due alberi AVL uno con chiavi tutte minori o maggiori dell'altro, ne restituisce un AVL
    Bilanciato e Concatenato
    :param A: ExtendedAVL - AVL Tree con chiavi tutte minori di B
    :param B: ExtendedAVL - AVL Tree con chiavi tutte maggiori di A
    :Time: O(log(n))
    :return:  ExtendedAVL - AVL Tree ( Concatenato )
    """

    # Ottengo l'altezza degli alberi
    H_a = A.getTreeHeight()
    H_b = B.getTreeHeight()

    if DEBUG:
        print "L'abero A ha altezza pari ad: " + str(H_a)
        print "L'albero B ha altezza pari ad: " + str(H_b)

    # Se uno dei due alberi dovesse avere altezza nulla restituisce l'altro albero
    # Se entrambi risultasseo avere altezze nulle allora ritorna None
    if H_a == None:
        return B
    elif H_b == None:
        return A
    elif H_a == None and H_b == None:
        return None

    # Punto Focale dell'algoritmo qui decide cosa fare
    # in base alla differente altezza dei due alberi
    if H_a <= H_b :
        # Ottengo il Nodo all'estrema destra di A
        R_a = A.getMaxNode()
        R_av = A.value(R_a)
        R_ak = A.key(R_a)


        # Rimuovo il Nodo dall'albero di A e Bilancio
        A.delete(A.key(R_a))

        if DEBUG:
            print("\n \n Massimo di A: \n")
            print(R_av)

            print("\n \n Albero A senza il suo Massimo \n")
            A.tree.stampa()


        # Cerco alla sinistra dell'albero più lungo, per ipotesi B un nodo la cui altezza
        # sia uguale o al limite di un'unità in più rispetto all'altezza dell'abero A
        R_b = B.searchLeftForNodeOfHeight(H_a)

        # Ottengo il padre di R_b così potrò attaccarvi il nodo precedentemente estratto da A
        if R_b.father == None:
            isRoot = True
            FtR_b = B.tree.root
        else:
            isRoot = False
            FtR_b = R_b.father

        # Rimuovo da B il Nodo R_b e ne estrapolo il sotto albero
        R_bt = B.tree.cut(R_b)
        if DEBUG:
            print("\n \n Sotto-albero del nodo R ( incluso ) \n \n")
            R_bt.stampa()

        # Ora creo un albero temporaneo in cui la radice è il massimo di A,
        # il suo figlio detro è l'intero sottoalbero di R_b ( incluso )
        # il suo filgio sinistro è l'intero albero A
        # tempA = createAVLByArray([R_av]) # vecchio metodo lasciato a testimonianza, per completezza
        # ho ritenuto di salvare, spero giustamente, anche il valore key precedente
        tempA = ExtendedAVL()
        tempA.insert(R_ak, R_av)
        tempA.tree.insertAsLeftSubTree(tempA.tree.root,A.tree)
        tempA.tree.insertAsRightSubTree(tempA.tree.root, R_bt)

        if DEBUG:
            print("\n \n Albero \"A\" Temporaneo \n \n")
            tempA.tree.stampa()

        # Aggiorno l'altezza di tale albero
        tempA.updateHeight(tempA.tree.root)

        if DEBUG:
            print("\n \n Altezza Aggioranta dell'Albero \"A\" Temporaneo \n \n")
            tempA.tree.stampa()

        if isRoot:
            return tempA    # se il nodo R risualtava essere proprio la radice di B
                            # è inutile innestare qualcosa in B se la stessa radice era il nodo R
                            # quindi ritorna direttamente l'albero temporaneo
        else:

            # Innesto quindi l'abero così creato in B
            # come sotto-albero sinistro del padre di R_b
            B.tree.insertAsLeftSubTree(FtR_b, tempA.tree)

            # Quindi aggiorno l'altezza del nodo a cui sono andato ad innestare
            # l'albero temporaneo precedentemente creato creato ad-hoc
            B.balInsert(FtR_b.leftSon)

            return B

    else:
        # Caso in cui H_a > H_b

        # Ottengo il Nodo all'estrema sinistra di B
        R_b = B.getMinNode()
        R_bv = B.value(R_b)
        R_bk = B.key(R_b)

        # Rimuovo il Nodo dall'albero di B e Bilancio
        B.delete(A.key(R_b))
        if DEBUG:
            print("\n \n Minimo di B \n" + str(R_bv))

            print("\n \n Albero B senza il suo minimo \n")
            B.tree.stampa()

        # Cerco alla destra dell'albero più lungo, per ipotesi A, un nodo la cui altezza
        # sia uguale o al limite di un'unità in più rispetto all'altezza dell'abero B
        R_a = A.searchRightForNodeOfHeight(H_b)

        # Ottengo il padre di R_a così potrò attaccarvi il nodo precedentemente estratto da B
        FtR_a = R_a.father

        # Rimuovo da B il Nodo R_b e ne estrapolo il sotto albero
        R_at = A.tree.cut(R_a)
        if DEBUG:
            print("\n \n Sotto-Albero R ( incluso ) \n \n")
            R_at.stampa()

        # Ora creo un albero temporaneo in cui la radice è il minimo di B,
        # il suo figlio detro è è l'intero albero B
        # il suo figlio sinistro è l'intero sottoalbero di R_a ( incluso )
        # tempB = createAVLByArray([R_bv]) # vecchio metodo lasciato a testimonianza, per completezza
        # ho ritenuto di salvare, spero giustamente, anche il valore key precedente
        tempB = ExtendedAVL()
        tempB.insert(R_bk, R_bv)
        tempB.tree.insertAsRightSubTree(tempB.tree.root, B.tree)
        tempB.tree.insertAsLeftSubTree(tempB.tree.root, R_at)

        if DEBUG:
            print("\n \n Albero \"B\" Temporaneo \n \n")
            tempB.tree.stampa()


        # Aggiorno l'altezza di tale albero
        tempB.updateHeight(tempB.tree.root)
        if DEBUG:
            print("\n \n Altezza aggiornata dell'Albero \"B\" Temporaneo \n \n")
            tempB.tree.stampa()

        # Innesto quindi l'abero così creato in B
        # come sotto-albero sinistro del padre di R_b
        A.tree.insertAsRightSubTree(FtR_a, tempB.tree)

        # Quindi aggiorno l'altezza del nodo a cui sono andato ad innestare
        # l'albero temporaneo precedentemente creato creato ad-hoc
        A.balInsert(FtR_a.rightSon)
        return A

