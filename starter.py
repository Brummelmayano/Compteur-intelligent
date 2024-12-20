import time
from afficheur import afficher_message  # Fonction pour afficher des messages sur la matrice LED
from video_utils import find_device_path, capture_image, verifier_similarite_frame

# Répertoire contenant les images de bruit de référence
repertoire_images_reference = "chemin/vers/repertoire_images_reference"

def starter():
    # Étape 1 : Récupération du périphérique vidéo
    device_path = find_device_path()
    if device_path is None:
        afficher_message("Aucune source video disponible")
        return

    # Étape 2 : Capture d'une image depuis le périphérique trouvé
    image_frame = capture_image(device_path)

    # Étape 3 : Vérification de la similarité avec les bruits
    resultat = verifier_similarite_frame(repertoire_images_reference, image_frame, seuil=0.8)
    
    if resultat:  # L'image capturée est similaire aux bruits
        afficher_message("Verifier le cable HDMI")
    else:  # L'image est claire, on lance le programme principal
        afficher_message("Lancement du programme...")
        import main  
        main.run()

if __name__ == "__main__":
    starter()
