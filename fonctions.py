import re

def filtrer_donnees_match(list_data, expression_reguliere):
    """
    Fonction pour filtrer une liste de données de match en fonction d'une expression régulière.

    Args:
        list_data: Liste de chaînes de caractères représentant les données du match.
        expression_reguliere: Expression régulière pour identifier les éléments valides.

    Returns:
        Liste des éléments valides extraits des données du match.
    """
    try:
        # Ignorer la casse
        regex = re.compile(expression_reguliere, re.IGNORECASE)

        # Filtrer les éléments en fonction de l'expression régulière
        donnees_valides = [element for element in list_data if regex.search(element)]

        return donnees_valides
    except re.error as e:
        print(f"Erreur dans l'expression régulière : {e}")
        return []
    except TypeError as e:
        print(f"Erreur de type : {e}")
        return []
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return []
