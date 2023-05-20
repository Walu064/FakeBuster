import csv
import os
import pytesseract
import pandas as pd
from googletrans import Translator

from langdetect import detect
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
    counter = 0
    for i in range(len(data)):
        try:
            conn = ocr(data[i]).replace('\n', ' ')
            # print("Conntekst: " + str(type(conn)) + ' -- ' + str(len(conn)))
            # lang = detect(conn)
            tran_conn = translate(conn, lang='pl')
            # print("trans: " + str(type(tran_conn)))
            df.loc[i, 'Path'] = data[i]
            df.loc[i, 'Content'] = tran_conn
            df.loc[i, 'Fake'] = 1
            # print(data[i])
            counter += 1
            print(counter)
        except Exception as e:
            print("ERROR: " + data[i] + " -- " + str(e))
            i -= 1
            # print(f'{conn = }')

    return df


def translate(text, lang):
    translator = Translator()
    return translator.translate(text, src=lang, dest='en').text
