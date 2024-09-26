import RPi.GPIO as GPIO  # Bibliothèque pour contrôler les GPIO du Raspberry Pi
import time  # Bibliothèque pour gérer le temps

# Configuration du bouton poussoir
BUTTON_PIN = 3  # Numéro du pin GPIO auquel le bouton est connecté

GPIO.setmode(GPIO.BCM)  # Utilisation du mode BCM pour les numéros de pin
GPIO.setwarnings(False)  # Désactiver les avertissements
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Configurer le pin comme entrée avec une résistance pull-up

def detect_button_press():
    """
    Fonction pour détecter l'appui du bouton poussoir et retourner un état en fonction
    de la durée pendant laquelle le bouton a été pressé.

    Retourne :
        - 1 si le bouton a été appuyé une fois (durée d'appui < 2 secondes)
        - 2 si le bouton a été maintenu pendant au moins 2 secondes mais moins de 5 secondes
        - 3 si le bouton a été maintenu pendant 5 secondes ou plus
    """
    start_time = 0  # Initialisation de la variable pour stocker le temps de début

    # Attente que le bouton soit pressé (GPIO passe à LOW quand le bouton est pressé)
    while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
        pass  # Boucle tant que le bouton n'est pas pressé

    start_time = time.time()  # Enregistrer le temps de début une fois le bouton pressé

    # Boucle tant que le bouton est maintenu pressé (GPIO reste LOW)
    while GPIO.input(BUTTON_PIN) == GPIO.LOW:
        pass  # Boucle tant que le bouton est toujours maintenu pressé

    press_duration = time.time() - start_time  # Calculer la durée pendant laquelle le bouton a été pressé

    # Retourne un résultat en fonction de la durée d'appui
    if press_duration < 2:
        return 1  # Bouton appuyé une fois (moins de 2 secondes)
    elif 2 <= press_duration < 5:
        return 2  # Bouton maintenu pendant au moins 2 secondes mais moins de 5 secondes
    else:
        return 3  # Bouton maintenu pendant 5 secondes ou plus
