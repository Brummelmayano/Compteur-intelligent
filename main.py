import time
from detect_roi import tflite_detect_and_cut_scoreboard
from capture_image import capture_image
from fonctions import filtrer_donnees_match, is_new_match, find_device_path, convertir_en_chaine
from ocr_paddle import ocr_paddle
from liste_chainee import ListeChainee
import cv2
from datetime import datetime
from afficheur_texte import AfficheurTexte
from files_manager import get_csv_last_match_counter, write_to_csv, get_csv_last_match_data
from bouton import demarrer_ecoute_bouton

def main():
    """
    Fonction principale pour exécuter le traitement des images et mettre à jour l'affichage du texte.

    Cette fonction capture des images en continu, détecte les régions d'intérêt, 
    extrait le texte à l'aide d'OCR, filtre les données extraites, et met à jour
    le compteur de matchs. Les résultats sont affichés sur une matrice LED et 
    les images pertinentes sont sauvegardées.
    """
        
    # Créer une liste chainé vide destiné à recevoir la liste [noms_equipes, score, minutes]
    liste = ListeChainee()

    #charger depuis le fichier csv le dernier enregistrement de type [noms_equipes, score, minutes]
    csv_last_match = get_csv_last_match_data()

    # Vérifier si csv_last_match n'est pas None avant de l'ajouter à la liste
    if csv_last_match is not None:
        liste.ajouter(csv_last_match)

    #obtenir match_counter du dernier match enregistré dans le fichier csv 
    match_counter = get_csv_last_match_counter()


    #recuperer le chemin ou l'index de l'HDMI VIDEO CAPTURE
    device_path = find_device_path()  

    # Créer une instance d'AfficheurTexte
    afficheur = AfficheurTexte(cascaded=2)

    # Mettre à jour le texte
    afficheur.mettre_a_jour_texte(f"{match_counter}")

    afficheur.demarrer() #damarrer l'afficheur avec l'objet crée dans un autre thread
    demarrer_ecoute_bouton(afficheur=afficheur)#demarrer l'écoute du bonton dans un autre thread

    while True:

        try:

            # 1. Capture d'image
            frame = capture_image(device_path)

            if frame is None:
                time.sleep(1)
                device_path = find_device_path()  
                raise Exception("Erreur lors de la capture d'image")

            # 2. Détection du ROI (Région d'Intérêt)
            cropped_image = tflite_detect_and_cut_scoreboard(image=frame)
            
            
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")  # Format de timestamp : année-mois-jour_heure-minute-seconde

            if cropped_image is None:
                nom_fichier = f"../images/captures/image_capturee_{timestamp}.jpg"  # à supprimer pendant le déploiement
                cv2.imwrite(nom_fichier, frame)
                print(f"Image enregistrée avec succès sous {nom_fichier}")

                raise Exception("Aucune bande de score détectée")

            # 3. Extraction de texte à l'aide d'un modèle OCR
            list_data = ocr_paddle(cropped_image)

            # Libérer la mémoire des images après utilisation
            del frame

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
            
            # Convertir les minutes actuelles et précédentes en secondes pour comparaison
            minutes_value = int(minutes[0].split(':')[0]) * 60 + int(minutes[0].split(':')[1])

            # ER pour les scores
            score_ER = r"^[0-9]{1}$"
            score = filtrer_donnees_match(list_data, score_ER)

            infos_detected = [noms_equipes, score, minutes]
            print(f"info détecté: {infos_detected}")

            # Ajouter les informations extraites seulement si les minutes sont extraites et si elle est comprise entre 05:00 et 130:00
            if (len(minutes[0]) == 5 or len(minutes[0]) == 4) and (5*60 <= minutes_value <= 135*60):
                # Écrire les informations extraites dans le fichier CSV
                write_to_csv(noms_equipes, score, minutes, afficheur.get_counter())

                liste.ajouter(infos_detected)
                liste.afficher()
                if liste.taille < 2:
                    afficheur.incremmenter()
                    print(f"Nouveau match détecté ! Compteur de match : {afficheur.get_counter()}")
                    print(f"Équipes : {noms_equipes}, Score : {score}, Minutes : {minutes}")
                    

                
                # Enregistre l'image (scoreboard) 
                infos_match = convertir_en_chaine(infos_detected)
                nom_fichier3 = f"../images/scoreboard_minutes_detected/{timestamp}__{infos_match}.jpg"  
                cv2.imwrite(nom_fichier3, cropped_image)
                print(f"Image enregistrée avec succès sous {nom_fichier3}")

            else:
                print("infos non ajoutées dans la liste")

            if liste.taille >= 2:
                previous_info = liste.recuperer_nieme_element(0)
                current_info = liste.recuperer_nieme_element(1)

                if is_new_match(current_info, previous_info):
                    afficheur.incremmenter()
                    print(f"Nouveau match détecté ! Compteur de match : {afficheur.get_counter()}")
                    print(f"Équipes : {noms_equipes}, Score : {score}, Minutes : {minutes}")
                    

                    infos_match = convertir_en_chaine(current_info)
                    nom_fichier2 = f"../images/nouveaux_match/{infos_match}.jpg"  

                    cv2.imwrite(nom_fichier2, cropped_image)
                    print(f"Image enregistrée avec succès sous {nom_fichier2}")
            
            # Supprimer l'image détectée dans la mémoire
            del cropped_image

            time.sleep(0.5)

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
