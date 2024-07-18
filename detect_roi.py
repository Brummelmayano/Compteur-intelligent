import cv2
import numpy as np
from tensorflow.lite.python.interpreter import Interpreter

# Définition de la fonction pour la détection et rognage avec le modèle TFLite
def tflite_detect_and_cut_scoreboard(image, modelpath="../model/detect.tflite", lblpath = '../model/labelmap.txt', min_conf=0.5):
    """
    Fonction pour détecter et rogner une zone spécifique (scoreboard) dans une image à l'aide d'un modèle TensorFlow Lite.

    Args:
        image: L'image source sous forme de tableau numpy.
        modelpath: Chemin vers le modèle TensorFlow Lite.
        lblpath: Chemin vers le fichier de labels (non utilisé dans cette fonction, mais inclus pour complétude).
        min_conf: Seuil de confiance minimum pour considérer une détection comme valide.

    Returns:
        Une image rognée de la zone détectée, ou None si aucune détection n'est valide.
    """
    try: 
        # Charger le modèle TensorFlow Lite en mémoire
        interpreter = Interpreter(model_path=modelpath)
        interpreter.allocate_tensors()

        # Récupération des détails du modèle
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        height = input_details[0]['shape'][1]
        width = input_details[0]['shape'][2]

        float_input = (input_details[0]['dtype'] == np.float32)

        input_mean = 127.5
        input_std = 127.5

        # Charger et traiter l'image par morceaux pour minimiser l'utilisation de la mémoire
        if image is None:
            print("Erreur lors du chargement de l'image. Vérifiez le chemin du fichier.")
            return None

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        imH, imW, _ = image.shape
        image_resized = cv2.resize(image_rgb, (width, height))
        input_data = np.expand_dims(image_resized, axis=0)

        if float_input:
            input_data = (np.float32(input_data) - input_mean) / input_std

        # Réalisation de la détection
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        # Récupération des résultats de détection
        boxes = interpreter.get_tensor(output_details[1]['index'])[0]
        classes = interpreter.get_tensor(output_details[3]['index'])[0]
        scores = interpreter.get_tensor(output_details[0]['index'])[0]

        # Boucle sur toutes les détections et traitement des résultats
        for i in range(len(scores)):
            if (scores[i] > min_conf) and (scores[i] <= 1.0):
                ymin = int(max(1, (boxes[i][0] * imH)))
                xmin = int(max(1, (boxes[i][1] * imW)))
                ymax = int(min(imH, (boxes[i][2] * imH)))
                xmax = int(min(imW, (boxes[i][3] * imW)))

                return image_rgb[ymin:ymax, xmin:xmax]

        return None
    except FileNotFoundError as e:
        print(f"Erreur de fichier non trouvé : {e}")
        return None
    except cv2.error as e:
        print(f"Erreur OpenCV : {e}")
        return None
    except Exception as e:
        print(f"Erreur lors de l'exécution de la détection : {e}")
        return None
