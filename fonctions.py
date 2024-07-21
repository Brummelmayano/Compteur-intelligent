import re
import cv2

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

    """""
    # Calculer le score total actuel et précédent en additionnant les scores individuels
    current_total_score = sum(map(int, current_score))
    previous_total_score = sum(map(int, previous_score))

    #les listes current_teams et previous_teams doivent contenir 2 deux equipes chacun 
    #et la longuer de current_score et previous_score
    if (len(current_teams) == 2) and  (len(previous_teams) == 2) and (len(current_score) == len(previous_score)):
      # Vérifier si les équipes ont changé ou si le score total actuel est inférieur au score total précédent
      if is_teams_changed(current_teams, previous_teams) or current_total_score < previous_total_score:
          return True  # Un nouveau match est détecté
    """""
    # current_minutes et previous_minutes doivent etre de meme longueur
    if len(current_minutes ) == len(previous_minutes):
      # Convertir les minutes actuelles et précédentes en secondes pour comparaison
      current_minutes_value = int(current_minutes[0].split(':')[0]) * 60 + int(current_minutes[0].split(':')[1])
      previous_minutes_value = int(previous_minutes[0].split(':')[0]) * 60 + int(previous_minutes[0].split(':')[1])

      # Vérifier si les minutes actuelles à partir de 05:00 sont inférieures aux minutes précédentes et qu'il n'est pas compris entre 45:00 et 55:00
      if (current_minutes_value < previous_minutes_value and 
          not (45*60 <= current_minutes_value <= 55*60) and 
          current_minutes_value >= 5*60):

          return True  # Un nouveau match est détecté

    return False  # Aucun nouveau match détecté



def find_device_path():
    """
    Cherche parmi plusieurs chemins de périphériques vidéo pour trouver celui
    qui peut être ouvert avec succès en utilisant OpenCV.

    Returns:
        str: Le chemin du périphérique vidéo disponible. Par défaut, retourne
             '/dev/video0' si aucun périphérique n'est trouvé.

    """
    device_paths = ['/dev/video0', '/dev/video1', '/dev/video2']

    for device_path in device_paths:
        # Tentative d'ouverture du périphérique vidéo avec OpenCV
        cap = cv2.VideoCapture(device_path, cv2.CAP_V4L2)
        if cap.isOpened():
            # Libération des ressources après vérification du succès de l'ouverture
            cap.release()
            return device_path

    # Si aucun périphérique n'est trouvé, retourne '/dev/video0' par défaut
    return '/dev/video0'



def convertir_en_chaine(liste):
    """
    Convertit toutes les informations d'une liste de listes en une seule chaîne de caractères.

    Chaque sous-liste de la liste principale est parcourue, chaque élément de la sous-liste
    est joint en une chaîne de caractères, et enfin toutes les sous-listes sont jointes
    en une seule chaîne de caractères.

    Paramètres:
    liste (list): Une liste de listes contenant des chaînes de caractères.

    Retourne:
    str: Une chaîne de caractères résultant de la concaténation de tous les éléments de la liste.

    Exemple:
    >>> liste = [['AVL', 'RMA'], ['0', '5'], ['01:24']]
    >>> convertir_en_chaine(liste)
    'AVL-RMA__0-5__01:24'
    """
    return '__'.join(['-'.join(sous_liste) for sous_liste in liste])