#afficheur_text.py

import os
import subprocess
import threading
import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, textsize, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
from luma.core.virtual import viewport



class AfficheurTexte:
    """
    Classe pour afficher du texte sur une matrice LED MAX7219.

    Cette classe gère l'affichage du texte sur un écran LED utilisant le contrôleur MAX7219. 
    Elle utilise un thread pour mettre à jour l'affichage en continu, et fournit des méthodes
    pour mettre à jour le texte à afficher et pour démarrer et arrêter le processus d'affichage.
    """

    def __init__(self, cascaded=2, mode_bouton = 1):
        """
        Initialise l'afficheur avec le nombre de matrices LED en cascade.

        :param cascaded: Le nombre de matrices LED connectées en cascade (par défaut 4).
        """

        # Tuer tous les processus utilisant SPI avant de démarrer
        self.terminer_processus_spi()

        # Configuration du port SPI pour le MAX7219
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, cascaded=cascaded, block_orientation=-90)
        self.device.contrast(5)
        self.texte = ""
        self.mode_bouton = mode_bouton
        self.lock = threading.Lock()
        self.thread_affichage = None  # Initialisation de l'attribut
        self.running = False  # Indicateur pour contrôler le thread
        self.stop_defilement = threading.Event()  # Événement pour stopper le défilement



    def afficher_texte(self):
        """
        Affiche le texte en continu sur la matrice LED.

        Si mode_bouton est égal à 1, affiche le texte.
        Si mode_bouton est égal à 2, initialise le texte à 0.
        """
        while self.running:
            with self.lock:
                if self.mode_bouton == 1:
                    # Mode d'affichage du texte
                    with canvas(self.device) as draw:
                        # Calcul de la largeur du texte pour centrer correctement
                        width, _ = textsize(self.texte, font=proportional(TINY_FONT))
                        x = (self.device.width - width) // 2
                        y = 0  # Position verticale fixe (en haut)

                        # Affichage du texte
                        text(draw, (x, y), self.texte, fill="white", font=proportional(TINY_FONT))
                elif self.mode_bouton == 2:
                    # Mode d'initialisation du compteur
                    self.initialiser()

            time.sleep(1)  # la pause

    def mettre_a_jour_texte(self, texte):
        """
        Met à jour le texte et redémarre immédiatement l'affichage.

        Si la longueur du texte est supérieure à 2, démarre le défilement.
        Sinon, affiche le texte statiquement.

        :param texte: Le nouveau texte à afficher.
        """
        with self.lock:
            self.texte = texte

        # Signale au défilement actuel de s'arrêter
        self.stop_defilement.set()

        # Attendre que le thread de défilement en cours s'arrête
        if hasattr(self, 'thread_defilement') and self.thread_defilement.is_alive():
            self.thread_defilement.join()

        # Réinitialiser l'événement de défilement
        self.stop_defilement.clear()

        # Choisir l'affichage selon la longueur du texte
        if len(texte) > 2:
            print("Texte long détecté, démarrage du défilement...")
            self.demarrer_defilement()
        else:
            print("Texte court détecté, affichage statique...")
            self.demarrer()



    def mettre_a_jour_mode_bouton(self, number):
        """
        Met à jour le numero qui a été appuyé par le bouton.

        :param number: l'entier qui a été retourné apres avoir appuyer le bouton
        """
        with self.lock:  #Lorsqu'un thread acquiert le verrou, les autres threads doivent attendre que ce verrou soit libéré avant de pouvoir accéder à la ressource.
            self.mode_bouton = number


    def demarrer(self):
        """
        Démarre le thread d'affichage du texte.

        Cette méthode crée et démarre un thread qui exécute `afficher_texte` en arrière-plan.
        Si le thread est déjà en cours d'exécution, cette méthode ne fait rien.
        """
        if not self.running:
            self.running = True
            self.thread_affichage = threading.Thread(target=self.afficher_texte)
            self.thread_affichage.daemon = True
            self.thread_affichage.start()

    def terminer_processus_spi(self):
        """
        Termine tous les processus utilisant les périphériques SPI.
        """
        try:
            # Lister tous les périphériques SPI disponibles
            spi_devices = ["/dev/spidev0.0", "/dev/spidev0.1", "/dev/spidev1.0", "/dev/spidev1.1", "/dev/spidev1.2"]

            # Pour chaque périphérique SPI, chercher les processus associés
            for device in spi_devices:
                result = subprocess.run(['lsof', device], capture_output=True, text=True)

                # Si des processus utilisent le périphérique, les tuer
                if result.stdout:
                    print(f"Processus trouvés pour {device} :\n{result.stdout}")
                    for line in result.stdout.splitlines()[1:]:  # Ignorer la première ligne (entête)
                        pid = int(line.split()[1])  # Le PID se trouve dans la deuxième colonne
                        print(f"Tuer le processus {pid} utilisant {device}")
                        os.kill(pid, 9)  # Tuer le processus avec signal 9 (SIGKILL)
        except Exception as e:
            print(f"Erreur lors de la terminaison des processus SPI : {e}")


    def arreter(self):
        """
        Arrête tous les threads en cours et nettoie les ressources.
        """
        self.running = False
        self.stop_defilement.set()  # Arrêter le défilement en cours
        if hasattr(self, 'thread_defilement') and self.thread_defilement.is_alive():
            self.thread_defilement.join()
        if self.thread_affichage and self.thread_affichage.is_alive():
            self.thread_affichage.join()
        self.device.clear()


    def initialiser(self):
        """
        Initialise l'attribut texte à 0.
        """
        with self.lock:
            self.texte = "0"
    
    def incremmenter(self):
        """
        Incrémente l'attribut texte de 1.
        """
        with self.lock:
            try:
                # Convertir le texte actuel en entier, incrémenter et reconvertir en chaîne de caractères
                valeur_actuelle = int(self.texte)
                self.texte = str(valeur_actuelle + 1)
            except ValueError:
                # Si le texte actuel ne peut pas être converti en entier, on initialise à 0 et on incrémente
                self.texte = "1"

    def get_counter(self):
        """
        Retourne l'attribut texte contenant la valeur du compteur sous forme d'entier.

        :return: La valeur de texte comme un entier, ou 0 si la conversion échoue.
        """
        with self.lock:
            try:
                return int(self.texte)
            except ValueError:
                return 0  # Retourne 0 si le texte ne peut pas être converti en entier
    
    def defiler_text(self, scroll_delay=0.07, font=proportional(TINY_FONT)):
        """
        Fait défiler le texte sur la matrice LED. Affiche chaque message en entier avant d'interrompre.

        :param scroll_delay: Le délai entre chaque mouvement du texte.
        :param font: La police à utiliser pour le texte.
        """
        while self.running and not self.stop_defilement.is_set():
            with self.lock:
                texte_a_defiler = self.texte

            # Vérifier si l'événement stop_defilement est activé avant de continuer
            if self.stop_defilement.is_set():
                break

            # Défilement complet du texte
            show_message(self.device, texte_a_defiler, fill="white", font=font, scroll_delay=scroll_delay)

            # Petite pause entre les répétitions
            time.sleep(0.1)




    def demarrer_defilement(self, scroll_delay=0.07, font=proportional(TINY_FONT)):
        """
        Démarre le thread pour faire défiler le texte sur la matrice LED.

        Utilise l'attribut `texte` pour le contenu à afficher.

        :param scroll_delay: Le délai entre chaque mouvement du texte.
        :param font: La police à utiliser pour le texte.
        """

        if not self.running:
            self.running = True
        self.thread_defilement = threading.Thread(
            target=self.defiler_text, args=(scroll_delay, font)
        )
        self.thread_defilement.daemon = True
        self.thread_defilement.start()


    def demarrer(self):
        """
        Démarre le thread d'affichage du texte.

        Cette méthode crée et démarre un thread qui exécute `afficher_texte` en arrière-plan.
        Si le thread est déjà en cours d'exécution, cette méthode ne fait rien.
        """
        if not self.running:        
            self.running = True
            if not self.thread_affichage or not self.thread_affichage.is_alive():
                self.thread_affichage = threading.Thread(target=self.afficher_texte)
                self.thread_affichage.daemon = True
                self.thread_affichage.start()
