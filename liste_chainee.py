#liste_chainee.py

class Noeud:
    """
    Cette classe représente un noeud d'une liste chaînée de valeurs.
    Chaque valeur est représentée par un tableau de trois éléments.
    """
    def __init__(self, valeur):
        if len(valeur) != 3:
            raise ValueError("La valeur doit être un tableau de trois éléments")

        self.valeur = valeur  # valeur est un tableau de trois éléments
        self.suivant = None

class ListeChainee:
    """
    Cette classe représente une liste chaînée de valeurs.
    Chaque valeur est représentée par un tableau de trois éléments.
    Cette classe permet d'ajouter des valeurs à la fin de la liste,
    La taille maximale de la liste est limitée à 5.
    Lorsque la taille dépasse 5, le plus ancien élément est supprimé.
    """

    def __init__(self):
        self.tete = None
        self.taille = 0  # Initialiser la taille à 0

    def ajouter(self, valeur):
        """
        Cette méthode permet d'ajouter une valeur à la fin de la liste.
        La valeur doit être un tableau de trois éléments.

        Args:
            valeur (list): La valeur à ajouter à la fin de la liste.
        """
        if len(valeur) != 3:
            raise ValueError("La valeur doit être un tableau de trois éléments")

        nouveau_noeud = Noeud(valeur)

        if self.tete is None:
            self.tete = nouveau_noeud
        else:
            # Parcourir la liste pour trouver le dernier noeud
            courant = self.tete
            while courant.suivant is not None:
                courant = courant.suivant

            # Ajouter le nouveau noeud à la fin
            courant.suivant = nouveau_noeud

        self.taille += 1

        # Si la taille dépasse 5, supprimer le premier noeud
        if self.taille > 2:
            self.supprimer_plus_vieux()

    def supprimer_plus_vieux(self):
        """
        Cette méthode supprime le premier noeud de la liste (le plus ancien)
        lorsque la taille dépasse 5.
        """
        if self.tete is None:
            return

        # Supprimer le premier noeud
        ancienne_tete = self.tete
        self.tete = self.tete.suivant
        ancienne_tete.suivant = None
        self.taille -= 1

    def recuperer_nieme_element(self, n):
        """
        Cette méthode permet de récupérer le n-ième élément de la liste.
        """
        if n < 0 or n >= self.taille:
            raise IndexError("Index hors limites")

        courant = self.tete
        indice = 0
        while indice < n:
            courant = courant.suivant
            indice += 1

        return courant.valeur

    def afficher(self):
        """
        Cette méthode affiche les valeurs de la liste chaînée.
        """
        courant = self.tete
        while courant is not None:
            print(courant.valeur, end=" -> ")
            courant = courant.suivant
        print("None")

    def taille(self):
        """
        Cette méthode retourne la taille actuelle de la liste chaînée.
        """
        return self.taille
