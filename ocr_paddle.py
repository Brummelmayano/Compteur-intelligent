#ocr_paddle.py

from paddleocr import PaddleOCR, draw_ocr

def ocr_paddle(image_path):
  """
  Fonction pour effectuer l'OCR avec PaddleOCR
  
  Args:
    image_path (str): image ou Chemin vers l'image à OCR
  
  Returns:
    values_list (list): Liste des valeurs extraites
  
  """

  # Initialiser PaddleOCR
  ocr = PaddleOCR(use_angle_cls=True, lang='en')

  # Effectuer l'OCR
  result = ocr.ocr(image_path, cls=True)

  # Récupérer le texte si le score est > 70% 
  values_list=[]
  for line in result:
      for word_info in line:
        if word_info[1][1]>0.7:
          values_list.append(word_info[1][0])
  
  return values_list
  