import csv
import os
import pytesseract
import pandas as pd

from langdetect import detect
from PIL import Image


def open_folder(path):
    result = []
    try:
        files = os.listdir(path)
        for file in files:
            result.append(path+'/'+file)
    except FileNotFoundError:
        print(f"Katalog o nazwie {path} nie istnieje.")
    return result


def OCR(image_path):
    image = Image.open(image_path)
    text_from_ocr = pytesseract.image_to_string(image)
    return text_from_ocr


def save_data_to_csv(data, path):
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data)


def prepare(data):
    df = pd.DataFrame({
        'Content': [],
        'Fake': [],
        'Language': []
    })
    for i in range(len(data)):
        df.loc[i, 'Content'] = OCR(data[i])
        df.loc[i, 'Fake'] = 1
        df.loc[i, 'Language'] = detect(df.loc[i, 'Content'])
    return df
