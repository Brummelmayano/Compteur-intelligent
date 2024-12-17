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

def comparer_histogrammes(hist1, hist2):
    """
    Compare deux histogrammes avec la méthode de corrélation.
    Retourne un score de similarité (plus proche de 1, plus similaire).
    """
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

def verifier_similarite(image_test_path, images_reference_paths, seuil=0.8):
    """
    Vérifie si une image de test est similaire à une liste d'images de référence.
    - seuil : score minimal pour être considéré comme similaire.
    """
    # Calculer l'histogramme de l'image test
    hist_test = calculer_histogramme(image_test_path)

    for ref_path in images_reference_paths:
        try:
            hist_ref = calculer_histogramme(ref_path)
            score = comparer_histogrammes(hist_test, hist_ref)
            print(f"Score de similarité avec {ref_path} : {score:.2f}")
            if score >= seuil:
                print("L'image test est similaire à une image bruitée de référence.")
                return True
        except FileNotFoundError as e:
            print(e)
    
    print("L'image test est considérée comme claire et différente des images bruitées.")
    return False
    


# Exemple d'utilisation
if __name__ == "__main__":
    # Chemins des images de référence (les 3 images bruitées)
    images_reference = [
        '/content/Image collée.png',
        '/content/Image collée (2).png',
        '/content/Image collée (3).png'
    ]

    # Chemin de l'image à tester
    image_test = '/content/image_capturee_2024-07-21_18-32-48.jpg'  # Remplacez par votre image à analyser

    # Vérification
    verifier_similarite(image_test, images_reference, seuil=0.8)
