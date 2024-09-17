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
        cap = cv2.VideoCapture(device_path, cv2.CAP_V4L2)
        
        # Vérifier si le périphérique vidéo est ouvert
        if not cap.isOpened():
            raise Exception("Assurez vous de mettre le bon index ou chemin de la capture video. \nVerifiez aussi que le repertoire'/dev' contient des autorisation possible ")
        
        # Attendre 2 secondes pour s'assurer que l'appareil soit prêt
        time.sleep(2)

        # Définir la résolution pour un format d'image 4:3 (par exemple, 640x480)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)   # Largeur de l'image
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)   # Hauteur de l'image

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

