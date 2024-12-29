#ouverture.py
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, CP437_FONT
import time
from fonctions import arreter_processus_spi
def ouverture():
    # Initialisation de l'afficheur
    arreter_processus_spi()
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=2, block_orientation=-90)
    device.contrast(1)  # Réduire le contraste

    # Boucle infinie pour afficher un message statique
    while True:
        with canvas(device) as draw:
            # Utilisation de 'text()' pour afficher le message avec une police prop>
            text(draw, (0, 0), " ...", fill="white", font=proportional(CP437_FONT))

        time.sleep(1)  # Pause pour maintenir le message affiché
        
        device.clear()

        time.sleep(1)  # Pause

ouverture()
        