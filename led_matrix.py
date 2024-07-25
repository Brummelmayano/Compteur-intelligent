import threading
import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, textsize
from luma.core.legacy.font import proportional, CP437_FONT

def afficher_texte_sur_max7219(texte, cascaded=4):
    """
    Affiche le texte spécifié sur un afficheur MAX7219.
    
    Args:
    - texte (str): Le texte à afficher sur l'afficheur.
    - cascaded (int, optional): Nombre de matrices MAX7219 en cascade (par défaut 4).
    """
    # Configuration du port SPI pour le MAX7219
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=cascaded, block_orientation=-90)
    device.contrast(5)

    # Calcul de la largeur du texte pour centrer correctement
    width, _ = textsize(texte, font=proportional(CP437_FONT))

    # Fonction pour afficher le texte en boucle
    def afficher_texte():
        while True:
            with canvas(device) as draw:
                # Calcul des coordonnées pour centrer le texte
                x = (device.width - width) // 2
                y = 0  # Position verticale fixe (en haut)

                # Affichage du texte
                text(draw, (x, y), texte, fill="white", font=proportional(CP437_FONT))

            time.sleep(1)  # Ajustez la pause selon vos besoins

    # Création et démarrage du thread pour l'affichage du texte
    thread_affichage = threading.Thread(target=afficher_texte)
    thread_affichage.start()
