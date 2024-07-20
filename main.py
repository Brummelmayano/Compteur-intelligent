from detect_roi import tflite_detect_and_cut_scoreboard
from capture_image import capture_image
from fonctions import filtrer_donnees_match, is_new_match, find_device_path

from ocr_paddle import ocr_paddle
from liste_chainee import ListeChainee
import cv2
from datetime import datetime


def main():
    # Créer une liste vide
    liste = ListeChainee()
    match_counter = 1
    device_path = find_device_path()  


    while True:
        try:
            # 1. Capture d'image
            frame = capture_image(device_path)

            if frame is None:
                raise Exception("Erreur lors de la capture d'image")

            # 2. Détection du ROI (Région d'Intérêt)
            cropped_image = tflite_detect_and_cut_scoreboard(image=frame)

            if cropped_image is None:
                now = datetime.now()
                timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")  # Format de timestamp : année-mois-jour_heure-minute-seconde
                nom_fichier = f"/images/captures/image_capturee_{timestamp}.jpg"
                cv2.imwrite(nom_fichier, frame)
                print(f"Image enregistrée avec succès sous {nom_fichier}")

                raise Exception("Aucune bande de score détectée")
                



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

            # Convertir chaque élément noms_equipes en majuscules
            noms_equipes = [nom_equipe.upper() for nom_equipe in noms_equipes]

            # ER pour le timing au format 00:00 et/ou 0:0
            minutes_ER = r"^\d{1,2}:\d{1,2}$"
            minutes = filtrer_donnees_match(list_data, minutes_ER)

            # ER pour les scores
            score_ER = r"^[0-9]{1}$"
            score = filtrer_donnees_match(list_data, score_ER)

            current_info = [noms_equipes, score, minutes]
            print(current_info)
            
            liste.ajouter(current_info)

            if liste.taille >= 2:
                previous_info = liste.recuperer_nieme_element(0)

                if is_new_match(current_info, previous_info):
                    match_counter += 1
                    print(f"Nouveau match détecté ! Compteur de match : {match_counter}")
                    print(f"Équipes : {noms_equipes}, Score : {score}, Minutes : {minutes}")

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

