import time
from afficheur_texte import AfficheurTexte
from fonctions import find_device_path
from calibrage import verifier_similarite_frame
from capture_image import capture_image

# Répertoire contenant les images de bruit de référence
repertoire_images_reference = "repertoire_images_reference"

def starter(afficheur):
    try:
        # Étape 1 : Récupération du périphérique vidéo
        device_path = find_device_path()
        if device_path is None:
            afficheur.mettre_a_jour_texte("Pas de source vidéo")
            return

        # Étape 2 : Capture d'une image depuis le périphérique trouvé
        image_frame = capture_image(device_path)

        # Vérification de l'image capturée
        if image_frame is None or image_frame.size == 0:
            afficheur.mettre_a_jour_texte("Erreur : Image non capturée")
            return

        # Étape 3 : Vérification de la similarité avec les bruits
        try:
            resultat = verifier_similarite_frame(repertoire_images_reference, image_frame, seuil=0.8)
        except Exception as e:
            afficheur.mettre_a_jour_texte(f"Erreur : {e}")
            return

        # Étape 4 : Actions en fonction du résultat
        if resultat:
            afficheur.mettre_a_jour_texte("Vérifier câble HDMI")
        else:
            afficheur.mettre_a_jour_texte("Lancement du programme...")
            import main
            main.run()

    except Exception as e:
        afficheur.mettre_a_jour_texte(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    afficheur = AfficheurTexte(cascaded=4, mode_bouton=1)
    #afficheur.demarrer()  # Démarre le thread d'affichage

    while True:
        starter(afficheur)
        time.sleep(2)  # Pause avant la prochaine exécution


