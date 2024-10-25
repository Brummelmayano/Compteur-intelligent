#bouton.py

import RPi.GPIO as GPIO  # Bibliothèque pour contrôler les GPIO du Raspberry Pi
import time  # Bibliothèque pour gérer le temps
import threading  # Bibliothèque pour gérer les threads

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

def ecouter(afficheur):
    """
    Fonction pour écouter en continu les appuis sur le bouton poussoir.

    Cette fonction tourne dans un thread séparé et met à jour le mode du bouton
    dans l'instance de AfficheurTexte via la méthode `mettre_a_jour_mode_bouton`.
    
    :param afficheur: L'instance de la classe AfficheurTexte.
    """
    while True:
        mode_bouton = detect_button_press()  # Obtenir l'état du bouton
        afficheur.mettre_a_jour_mode_bouton(mode_bouton)  # Mettre à jour le mode dans l'afficheur
        time.sleep(0.1)  # Petite pause pour éviter une boucle trop rapide

def demarrer_ecoute_bouton(afficheur):
    """
    Démarre un thread pour écouter les appuis du bouton.

    :param afficheur: L'instance de la classe AfficheurTexte.
    """
    thread_bouton = threading.Thread(target=ecouter, args=(afficheur,))
    thread_bouton.daemon = True  # Permet au thread de se fermer quand le programme principal se termine
    thread_bouton.start()
