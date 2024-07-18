from detect_roi import tflite_detect_and_cut_scoreboard
from capture_image import capture_image
from fonctions import filtrer_donnees_match
from ocr_paddle import ocr_paddle
from liste_chainee import ListeChainee


def main():
    #creer une liste vide
    liste = ListeChainee()

    while True:
        try:
            # 1. Capture d'image
            device_path = '/dev/video0'  # Remplacez par le chemin correct
            frame = capture_image(device_path)

            if frame is None:
                raise Exception("Erreur lors de la capture d'image")

            # 2. Détection du ROI (Région d'Intérêt)
            cropped_image = tflite_detect_and_cut_scoreboard(image=frame)

            if cropped_image is None:
                raise Exception("Aucune bande de score detecté")

            # 3. Extraction de texte à l'aide d'un modèle OCR
            list_data = ocr_paddle(cropped_image)

            # Libérer la mémoire des images après utilisation
            del frame
            del cropped_image

            if not list_data:
                raise Exception("Erreur lors de l'extraction de texte avec OCR")

            # 4. Filtrage de texte à l'aide d'une expression régulière
            # ER pour les noms d'équipes de 2 ou 3 lettres
            equipes_ER = r".*^[A-Za-z]{2,3}$"
            noms_equipes = filtrer_donnees_match(list_data, equipes_ER)

            # ER pour le timing au format 00:00 et/ou 0:0
            minutes_ER = r"^\d{1,2}:\d{1,2}$"
            minutes = filtrer_donnees_match(list_data, minutes_ER)

            # ER pour les scores
            score_ER = r"^[0-9]{1,2}$"
            score = filtrer_donnees_match(list_data, score_ER)

            liste.ajouter([noms_equipes, score, minutes])

        except Exception as e:
            print(f"Erreur : {e}")

        finally:
            # Assurer la libération de la mémoire
            if 'frame' in locals():
                del frame
            if 'cropped_image' in locals():
                del cropped_image
            if 'list_data' in locals():
                del list_data

if __name__ == "__main__":
    main()

