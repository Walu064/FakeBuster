import os
import cv2
from PIL import Image
import pytesseract
from langdetect import detect
from googletrans import Translator
import nltk
import nltk.corpus
import sklearn

# Ads detection Selenium (Czy tam coś), potem OpenCV i wycięcie posta z reklamą.

# OCR: 
image_path = 'obraz_mati.jpg'
image = Image.open(image_path)
text_from_ocr = pytesseract.image_to_string(image, lang="pol")
print("Original text from OCR: ")
print(text_from_ocr)

# Language detection:
detected_language = detect(text_from_ocr)

# Text translation:
translator = Translator()
translated_text_from_ocr = translator.translate(text_from_ocr, src=detected_language, dest='en').text

# Test:
print("Detected language: "+detected_language)
print("Translated text from OCR: ")
print(translated_text_from_ocr)

# Tu się zaczyna zabawa w NLP.


##  To do:
#   ads detection (Kręgiel)
#   NLP (Walu, Góral)
#   Classification (Jastrzymbie)
#   Integration (Autisto)
#   Trucie dupska mentorom, naruchiwanie danych do uczenia (Targos123)