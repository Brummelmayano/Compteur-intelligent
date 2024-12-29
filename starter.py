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
            afficheur.mettre_a_jour_texte("PAS DE SOURCE VIDEO")
            return

        # Étape 2 : Capture d'une image depuis le périphérique trouvé
        image_frame = capture_image(device_path)

        # Vérification de l'image capturée
        if image_frame is None or image_frame.size == 0:
            print("Erreur : Image non capturée")
            return
        else:
            afficheur.mettre_a_jour_texte("TRAITEMENT DE L'IMAGE...")

            

        # Étape 3 : Vérification de la similarité avec les bruits
        try:
            resultat = verifier_similarite_frame(repertoire_images_reference, image_frame, seuil=0.8)
        except Exception as e:
            print(f"Erreur : {e}")
            return

        # Étape 4 : Actions en fonction du résultat
        if resultat:
            afficheur.mettre_a_jour_texte("VERIFIER LA SOURCE VIDEO")
        else:
            afficheur.mettre_a_jour_texte("LANCEMENT...")
            import main
            main.run()

    except Exception as e:
        print(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    afficheur = AfficheurTexte(cascaded=2, mode_bouton=1)
    #afficheur.demarrer()  # Démarre le thread d'affichage

    while True:
        starter(afficheur)
        time.sleep(2)  # Pause avant la prochaine exécution


