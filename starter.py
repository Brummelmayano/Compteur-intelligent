import time
from afficheur_texte import AfficheurTexte
from fonctions import find_device_path
from calibrage import verifier_similarite_frame
from capture_image import capture_image
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT



# Arrêter l'affichage du texte

#afficheur.arreter()  # Arrêter le processus



# Répertoire contenant les images de bruit de référence
repertoire_images_reference = "repertoire_images_reference"

def starter():


    afficheur = AfficheurTexte(cascaded=4, mode_bouton=1)

    # Afficher le premier texte
    afficheur.mettre_a_jour_texte("Nouveau a afficher")
    afficheur.demarrer_defilement(scroll_delay=0.1)

    # Pause pour laisser défiler
    time.sleep(2)

    # Mettre à jour le texte
    afficheur.mettre_a_jour_texte("papa et maman")

    # Pause pour observer le deuxième texte
    time.sleep(2)

    # Arrêter l'afficheur
    afficheur.arreter()

    
    # Étape 1 : Récupération du périphérique vidéo
    #device_path = find_device_path()
    #if device_path is None:
        #afficheur.mettre_a_jour_texte("Aucune source vidéo disponible")
        #return

    # Étape 2 : Capture d'une image depuis le périphérique trouvé
    #image_frame = capture_image(device_path)

    # Vérification de l'image capturée
    #if image_frame is None or image_frame.size == 0:
        #afficheur.mettre_a_jour_texte("Erreur : Aucune image capturée. Vérifiez le périphérique vidéo.")
        #return

    # Étape 3 : Vérification de la similarité avec les bruits
    #try:
        #resultat = verifier_similarite_frame(repertoire_images_reference, image_frame, seuil=0.8)
    #except Exception as e:
        #afficheur.mettre_a_jour_texte(f"Erreur : {e}")
        #return

    #if resultat:  # L'image capturée est similaire aux bruits
        #afficheur.mettre_a_jour_texte("Vérifier le câble HDMI")
    #else:  # L'image est claire, on lance le programme principal
        #afficheur.mettre_a_jour_texte("Lancement du programme...")
        #import main
        #main.run()


if __name__ == "__main__":
    while True:
        starter()
