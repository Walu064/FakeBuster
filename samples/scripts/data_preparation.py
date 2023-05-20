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
    iter = 0
    err_iter = 0
    df_test_data = pd.read_csv('test_data.csv')
    column_path = df_test_data['Path']


    while True:
        tran_conn = ''
        try:
            if iter == len(data):
                break
            if data[iter] in column_path:
                print("Wykryto plik: " + data[iter])
                continue
            conn = ocr(data[iter]).replace('\n', ' ')
            # lang = detect(conn)
            tran_conn = translate(conn, lang='pl')
            # print("trans: " + str(type(tran_conn)))
            # print(data[i])
            df.loc[iter, 'Path'] = data[iter]
            df.loc[iter, 'Content'] = tran_conn
            df.loc[iter, 'Fake'] = 1
            print(str(iter) + " -- " + str(data[iter]))
            iter += 1
            err_iter = 0
        except Exception as e:
            err_iter += 1
            if err_iter > 20:
                iter += 1
            print("ERROR: " + data[iter] + " -- " + str(e))

            # print(f'{conn = }')
    return df


def translate(text, lang):
    translator = Translator()
    return translator.translate(text, src=lang, dest='en').text
