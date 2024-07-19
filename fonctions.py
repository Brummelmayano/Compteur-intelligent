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

def is_teams_changed (liste1, liste2):
  """
  verifie si les équipes ont changé

  Args:
    liste1 (list): liste des équipes capturé precedemment
    liste2 (list): liste des équipes capturé maintenant
  Returns:
    bool: True si les équipes ont changé, False sinon

  """
  if liste1 == liste2:
    return False
  return True


def is_teams_changed(current_teams, previous_teams):
    """
    verifie si les équipes ont changé

    Args:
        previous_teams (list): liste des équipes capturé precedemment
        current_teams (list): liste des équipes capturé actuellement
    Returns:
        bool: True si les équipes ont changé, False sinon

    """
    return current_teams != previous_teams


def is_new_match(current_info, previous_info):
    """
    Détermine si un nouveau match a commencé en comparant les informations actuelles et précédentes.

    Args:
        current_info (list): Informations actuelles sous la forme [noms_équipes, score, minutes].
        previous_info (list): Informations précédentes sous la forme [noms_équipes, score, minutes].

    Returns:
        bool: True si un nouveau match est détecté, sinon False.
    """
    # Décomposer les informations actuelles et précédentes en équipes, scores et minutes
    current_teams, current_score, current_minutes = current_info
    previous_teams, previous_score, previous_minutes = previous_info

    # Calculer le score total actuel et précédent en additionnant les scores individuels
    current_total_score = sum(map(int, current_score))
    previous_total_score = sum(map(int, previous_score))

    # Vérifier si les équipes ont changé ou si le score total actuel est inférieur au score total précédent
    if is_teams_changed(current_teams, previous_teams) or current_total_score < previous_total_score:
        return True  # Un nouveau match est détecté

    # Convertir les minutes actuelles et précédentes en valeurs numériques pour comparaison
    current_minutes_value = int(current_minutes[0].split(':')[0]) * 60 + int(current_minutes[0].split(':')[1])
    previous_minutes_value = int(previous_minutes[0].split(':')[0]) * 60 + int(previous_minutes[0].split(':')[1])

    # Vérifier si les minutes actuelles sont inférieures aux minutes précédentes
    if current_minutes_value < previous_minutes_value:
        return True  # Un nouveau match est détecté

    return False  # Aucun nouveau match détecté
