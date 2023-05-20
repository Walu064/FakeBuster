import os
import cv2
from PIL import Image
import pytesseract
from langdetect import detect
from googletrans import Translator
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Ads detection Selenium (Czy tam coś), potem OpenCV i wycięcie posta z reklamą.

# OCR: 
# image_path = 'obraz_mati.jpg'
# image = Image.open(image_path)
# text_from_ocr = pytesseract.image_to_string(image, lang="pol")
# print("Original text from OCR: ")
# print(text_from_ocr)

text_from_ocr = "Gorące Mamuśki w twojej okolicy! Powiększ penisa! +20cm w miesiąc!"
# Language detection:
detected_language = detect(text_from_ocr)

# Text translation:
translator = Translator()
translated_text_from_ocr = translator.translate(text_from_ocr, src=detected_language, dest='en').text

# Test:
print("Detected language: "+detected_language)
print("Translated text from OCR: ")
print(translated_text_from_ocr)

# Stopword list download:
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Funkcja preprocessingu tekstu
def preprocess_text(text):
    # Tokenizacja tekstu
    tokens = word_tokenize(text)
    # Usunięcie stopwords
    tokens = [token for token in tokens if token.lower() not in stop_words]
    # Lematyzacja
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    # Połączenie tokenów z powrotem w tekst
    processed_text = ' '.join(tokens)
    return processed_text

print(preprocess_text(translated_text_from_ocr))