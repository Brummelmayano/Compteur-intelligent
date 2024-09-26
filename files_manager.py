import csv
from datetime import datetime

def get_csv_last_match_counter(csv_file='matches.csv'):
    """
    Récupère la dernière valeur de match_counter depuis le fichier CSV.

    Args:
        csv_file (str): Chemin vers le fichier CSV.

    Returns:
        int: La dernière valeur de match_counter trouvée dans le fichier CSV, ou 0 si le fichier est vide.
    """
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            last_row = list(reader)[-1]  # Obtenir la dernière ligne
            if last_row:
                return int(last_row[4])  # Supposant que match_counter est la 5ème colonne
    except (IndexError, FileNotFoundError):
        return 0  # Retourner 0 si le fichier est vide ou non trouvé

    return 0

def write_to_csv(team_names, score, minutes, match_counter):
    """
    Écrit les informations du match dans un fichier CSV.

    Args:
        team_names (list): Liste des noms des équipes.
        score (list): Liste des scores.
        minutes (list): Liste des minutes.
        match_counter (int): Valeur actuelle du compteur de matchs.
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")  # Format de la date et de l'heure
    with open('matches.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date_str, team_names, score, minutes, match_counter])


def get_csv_last_match_data(csv_file='matches.csv'):
    """
    Récupère les données de la dernière ligne du fichier CSV.

    Args:
        csv_file (str): Chemin vers le fichier CSV.

    Returns:
        tuple: Les données de la dernière ligne sous forme d'une liste [noms_equipes, score, minutes].
               Retourne None si le fichier est vide ou non trouvé.
    """
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            last_row = list(reader)[-1]  # Obtenir la dernière ligne

            if last_row:
                team_names = last_row[1]
                team_names_list = ast.literal_eval(team_names_str)

                score = last_row[2]
                score_list = ast.literal_eval(score)

                minutes = last_row[3]
                minutes_list = ast.literal_eval(minutes)
                return [team_names_list, score_list, minutes_list]
    
    except (IndexError, FileNotFoundError):
        return None  # Retourner None si le fichier est vide ou non trouvé

