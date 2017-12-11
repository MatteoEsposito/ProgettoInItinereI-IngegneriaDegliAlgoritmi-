# coding=utf-8
from DicionaryAVL import DictAVL


class ExtendedAVL(DictAVL):

    def __init__(self):
        DictAVL.__init__(self)

    def getTreeHeight(self):
        """
        Ottengo altezza dell'albero con una shortcut ( ottengo semplicemente l'altezza della Radice )
        ovviamente questa funzione è semplceimente il richiamo alla funzione height sulla radice
        a sè stante non aggiunge ne estende nulla di che ma l'ho ritenuta comuqnue utile
        al fine di facilitare la comprensione del main code a prima vista

        :Time: O(1)
        :return: int
        """

        return self.height(self.tree.root)

    # Il Seguente set di funzioni sono utili nel caso in cui l'altezza di B sia maggiore dell'altezza di A
    def getMaxNode(self):
        """
        Scendo dall'albero verso destra per ottenre il massimo valore salvato nell'AVL
        :Time: O(log(n)), dato il fatto che l'albero AVL ha, per definizione, un'altezza pari a log(n)
                          nel peggiore scenario esso scenderà per un albero di altezza log(n)
        :return: Max Node
        """

        curr = self.tree.root

        while curr.rightSon != None:
            curr = curr.rightSon

        return curr

    def searchLeftForNodeOfHeight(self, height):
        """
        Cerco verso sinistra il primo nodo la cui altezza sia uguale all'altezza cercata
        o al massimo di una singola unità più alta
        :param height: int, altezza che voglio cercare
        :Time: O(log(n)), dato il fatto che l'albero AVL ha, per definizione, un'altezza pari a log(n)
                          nel peggiore scenario esso scenderà per un albero di altezza log(n)
        :return: AVL Tree Node
        """

        curr = self.tree.root

        while self.height(curr) != height and self.height(curr) != height+1: # Scandisce fino a trovare un nodo con altezza
            if curr.leftSon  == None:                                        # uguale o +1 di quela specficata quindi interrompe
                break                                                        # il ciclo
            else:
                curr = curr.leftSon

        if self.height(curr.leftSon) == height:     # il ciclo potrebbe essersi fermato ad h+1 però magari esisteva un nodo
            return curr.leftSon                     # con h == height quinid fa un breve check. Se il risultato del check
        else:                                       # è positivo allora ritorna il successivo altrimenti ritorna il corrente
            return curr


    # Il Seguente set di funzioni sono utili nel caso in cui l'altezza di A sia maggiore dell'altezza di B
    def getMinNode(self):
        """
        Scendo dall'alabero verso sinistra per ottenre il minimo valore salvato nell'AVL
        :Time: O(log(n)), dato il fatto che l'albero AVL ha, per definizione, un'altezza pari a log(n)
                          nel peggiore scenario esso scenderà per un albero di altezza log(n)
        :return: Min Node
        """

        curr = self.tree.root

        while curr.leftSon != None:
            curr = curr.leftSon

        return curr

    def searchRightForNodeOfHeight(self, height):
        """
        Cerco verso destra il primo nodo la cui altezza sia uguale all'altezza cercata
        o al massimo di una singola unità più alta
        :param height: int, altezza che voglio cercare
        :Time: O(log(n)), dato il fatto che l'albero AVL ha, per definizione, un'altezza pari a log(n)
                          nel peggiore scenario esso scenderà per un albero di altezza log(n)
        :return: AVL Tree Node
        """

        curr = self.tree.root

        while self.height(curr) != height and self.height(curr) != height+1:    # Scandisce fino a trovare un nodo con altezza
            curr = curr.rightSon                                                # uguale o +1 di quela specficata quindi interrompe
                                                                                # il ciclo

        if self.height(curr.rightSon) == height or  self.height(curr.rightSon) == height+1 :  # il ciclo potrebbe essersi fermato ad h+1 però magari esisteva un nodo
            return curr.rightSon                                                              # con h == height quinid fa un breve check. Se il risultato del check
        else:                                                                                 # è positivo allora ritorna il successivo altrimenti ritorna il corrente
            return curr

