import threading
import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, textsize
from luma.core.legacy.font import proportional, CP437_FONT

class AfficheurTexte:
    """
    Classe pour afficher du texte sur une matrice LED MAX7219.

    Cette classe gère l'affichage du texte sur un écran LED utilisant le contrôleur MAX7219. 
    Elle utilise un thread pour mettre à jour l'affichage en continu, et fournit des méthodes
    pour mettre à jour le texte à afficher et pour démarrer et arrêter le processus d'affichage.
    """

    def __init__(self, cascaded=4, mode_bouton = 1):
        """
        Initialise l'afficheur avec le nombre de matrices LED en cascade.

        :param cascaded: Le nombre de matrices LED connectées en cascade (par défaut 4).
        """
        # Configuration du port SPI pour le MAX7219
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, cascaded=cascaded, block_orientation=-90)
        self.device.contrast(5)
        self.texte = ""
        self.mode_bouton = mode_bouton
        self.lock = threading.Lock()
        self.thread_affichage = None  # Initialisation de l'attribut
        self.running = False  # Indicateur pour contrôler le thread

    def afficher_texte(self):
        """
        Affiche le texte en continu sur la matrice LED.

        Cette méthode est exécutée dans un thread en arrière-plan. Elle dessine le texte
        centré horizontalement et fixe verticalement, puis attend une seconde avant de
        redessiner le texte.
        """
        while self.running:
            with self.lock:
                with canvas(self.device) as draw:
                    # Calcul de la largeur du texte pour centrer correctement
                    width, _ = textsize(self.texte, font=proportional(CP437_FONT))
                    x = (self.device.width - width) // 2
                    y = 0  # Position verticale fixe (en haut)

                    # Affichage du texte
                    text(draw, (x, y), self.texte, fill="white", font=proportional(CP437_FONT))
            time.sleep(1)  # Ajustez la pause selon vos besoins

    def mettre_a_jour_texte(self, texte):
        """
        Met à jour le texte à afficher sur la matrice LED.

        :param texte: Le nouveau texte à afficher.
        """
        with self.lock:  #Lorsqu'un thread acquiert le verrou, les autres threads doivent attendre que ce verrou soit libéré avant de pouvoir accéder à la ressource.
            self.texte = texte
    
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

    def arreter(self):
        """
        Arrête le thread d'affichage du texte et nettoie les ressources.

        Cette méthode arrête le thread en changeant la variable `self.running`, attend que le
        thread se termine, puis efface l'affichage et nettoie les ressources du périphérique.
        """
        self.running = False
        if self.thread_affichage:
            self.thread_affichage.join()  # Attend que le thread se termine
        self.device.clear()
        self.device.cleanup()


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
