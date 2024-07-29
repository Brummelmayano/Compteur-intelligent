import cv2
import time

def capture_image(device_path):
    """
    Fonction pour capturer une image à partir d'un périphérique vidéo.

    Args:
        device_path: Chemin vers le périphérique vidéo (par exemple, '/dev/video0').

    Returns:
        frame: L'image capturée sous forme de tableau numpy.
    """
    try:
        # Ouvrir le périphérique vidéo
        cap = cv2.VideoCapture(device_path)
        # Vérifier si la vidéo est correctement ouverte
        if not cap.isOpened():
            print("Erreur: Impossible d'ouvrir la vidéo.")
        else:
            print("Vidéo ouverte avec succès.")

	# Temps en millisecondes où vous voulez capturer l'image (par exemple, 5000 ms = 5 secondes)
        temps_de_capture_ms = temps_de_capture_ms + 50000

	# Définir la position de la vidéo au temps désiré
        cap.set(cv2.CAP_PROP_POS_MSEC, temps_de_capture_ms)
	
        # Capturer une image
        ret, frame = cap.read()
        
        if not ret:
            raise Exception("essayer de débrancher puis rebrancher le HDMI Video Capture")
        
        # Libérer les ressources
        cap.release()
        print(f"Image {device_path} capturée")
        
        return frame

    except Exception as e:
        print(f"quelque chose s'est mal passé lors de la capture d'image : {e}")
        # Libérer les ressources si une exception est levée
        if cap and cap.isOpened():
            cap.release()

