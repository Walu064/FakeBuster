import os
import pytesseract
import pandas as pd
from PIL import Image


def open_folder(path):
    result = []
    try:
        files = os.listdir(path)
        for file in files:
            result.append(path + '/' + file)
    except FileNotFoundError:
        print(f"Katalog o nazwie {path} nie istnieje.")
    return result


def ocr(image_path) -> str:
    image = Image.open(image_path)
    text_from_ocr = pytesseract.image_to_string(image, lang="pol")
    return text_from_ocr


def prepare(data):
    df = pd.DataFrame({
        'Path': [],
        'Content': [],
        'Fake': []
    })
    for i in range(len(data)):
        try:
            conn = ocr(data[i]).replace('\n', ' ')
            print("Conntekst: " + str(type(conn)) + ' -- ' + str(len(conn)))
            print("trans: " + str(type(conn)))
            df.loc[i, 'Path'] = data[i]
            df.loc[i, 'Content'] = conn
            df.loc[i, 'Fake'] = 1
            print(data[i])
        except Exception as e:
            print("ERROR: " + data[i] + " -- " + str(e))
            print(f'{conn = }')
    return df


