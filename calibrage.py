import cv2
import numpy as np
import os

def calculer_histogramme(image_path):
    """
    Calcule l'histogramme normalisé d'une image en niveaux de gris.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Impossible de charger l'image : {image_path}")

    # Calculer l'histogramme
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    hist = cv2.normalize(hist, hist).flatten()  # Normaliser l'histogramme
    return hist

def calculer_histogramme_frame(frame):
    """
    Calcule l'histogramme normalisé d'une image frame (NumPy array) en niveaux de gris.
    """
    image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([image_gray], [0], None, [256], [0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist

def comparer_histogrammes(hist1, hist2):
    """
    Compare deux histogrammes avec la méthode de corrélation.
    Retourne un score de similarité (plus proche de 1, plus similaire).
    """
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

def verifier_similarite_frame(repertoire_images_reference, image_frame, seuil=0.8):
    """
    Vérifie si une image frame est similaire à des images contenues dans un répertoire de référence.
    - repertoire_images_reference : chemin du répertoire contenant les images de référence
    - image_frame : image à comparer sous forme de tableau NumPy
    - seuil : score minimal pour être considéré comme similaire
    Retourne True si une similarité est détectée, sinon False.
    """
    # Vérifier si le répertoire existe
    if not os.path.exists(repertoire_images_reference):
        raise FileNotFoundError(f"Le répertoire spécifié est introuvable : {repertoire_images_reference}")

    # Récupérer les chemins des images dans le répertoire
    images_reference_paths = [
        os.path.join(repertoire_images_reference, file)
        for file in os.listdir(repertoire_images_reference)
        if file.endswith(('.png', '.jpg', '.jpeg'))
    ]

    # Calculer l'histogramme de l'image frame
    hist_test = calculer_histogramme_frame(image_frame)

    for ref_path in images_reference_paths:
        try:
            hist_ref = calculer_histogramme(ref_path)
            score = comparer_histogrammes(hist_test, hist_ref)
            print(f"Score de similarité avec {ref_path} : {score:.2f}")
            if score >= seuil:
                print("L'image frame est similaire à une image bruitée de référence.")
                return True
        except FileNotFoundError as e:
            print(e)

    print("L'image frame est considérée comme claire et différente des images bruitées.")
    return False
