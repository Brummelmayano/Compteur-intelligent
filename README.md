# Compteur-intelligent

Compteur intelligent des matchs dans une salle de jeux vidéo

Ce projet a pour objectif de compter automatiquement les matchs de foot joués dans une console. 
Le système utilise des modeles de detection d'objet, de reconnaissance optique de caractères (OCR) et des expression régulière pour détecter, extraire puis filtrer le texte obtenu. 

## Installation

Pour installer les dépendances nécessaires, exécutez la commande suivante :

```sh
pip install -r requirements.txt
```

### Fonction principale à éxecuter (main.py)

Ce fichier contient le script principal pour exécuter le programme de comptage de matchs.

- `main()`: La fonction principale qui coordonne les différentes étapes du processus de comptage de matchs :
  1. Capture d'image : Capture une image depuis le périphérique vidéo.
  2. Détection de la ROI : Utilise le modèle TensorFlow Lite pour détecter la région d'intérêt dans l'image.
  3. OCR : Utilise PaddleOCR pour extraire le texte de la région d'intérêt.
  4. Filtrage des données : Filtre les données extraites pour identifier les informations pertinentes sur les matchs.
  5. Affichage des résultats : Affiche le n ieme match sur un Matrix LED Display MAX7219 8x16

```sh
python3 main.py
```


## Description des fichiers

### detect_roi.py

Ce fichier contient des fonctions pour détecter et rogner une zone spécifique (scoreboard) dans une image en utilisant un modèle TensorFlow Lite.

- `tflite_detect_and_cut_scoreboard(image, modelpath, lblpath, min_conf)`: Cette fonction utilise un modèle TensorFlow Lite pour détecter la région d'intérêt (ROI) correspondant au tableau de scores dans une image. Les paramètres incluent le chemin du modèle, le chemin du fichier de label et une confiance minimale pour la détection.

### capture_image.py

Ce fichier contient des fonctions pour capturer des images à partir d'un périphérique vidéo.

- `capture_image(device_path)`: Cette fonction capture une image depuis un périphérique vidéo spécifié par `device_path` (par exemple, '/dev/video0'). Elle retourne l'image capturée sous forme de tableau numpy.

### fonctions.py

Ce fichier contient des fonctions utilitaires pour filtrer les données de match.

- `filtrer_donnees_match(list_data, expression_reguliere)`: Filtre une liste de données de match en fonction d'une expression régulière.
- `is_new_match(data)`: Vérifie si les données fournies représentent un nouveau match.

### ocr_paddle.py

Ce fichier contient des fonctions pour effectuer la reconnaissance optique de caractères (OCR) avec PaddleOCR.

- `ocr_paddle(image_path)`: Cette fonction effectue l'OCR sur une image spécifiée par `image_path`. Elle retourne une liste des valeurs extraites à partir de l'image.

### liste_chainee.py

Ce fichier définit les classes pour la gestion d'une liste chaînée de valeurs.

- `class Noeud`: Représente un noeud d'une liste chaînée. Chaque noeud contient une valeur (un tableau de trois éléments) et un pointeur vers le noeud suivant.
- `class ListeChainee`: Représente une liste chaînée de valeurs. Elle permet d'ajouter des noeuds et de parcourir la liste.

### afficheur_texte.py

Ce fichier contient des fonctions pour afficher les textes extraits sur un écran ou une interface utilisateur.

- `afficher_texte(texte)`: Affiche le n ieme match sur un Matrix LED Display MAX7219 8x16

