import pandas as pd
from fakebuster.classification_model.SVM_pred import predict

from samples.scripts.data_preparation import open_folder, prepare

path = "Reklamy"

if __name__ == "__main__":
        paths_of_file = open_folder(path)
        # print(paths_of_file)
        df = prepare(paths_of_file)
        print(df)
    
''' przykład wywołania predict przyjmuje ramkę danych
        text = pd.read_csv('E:\Hackathon\supervision2\FakeBuster\samples\data\learn_legit_data.csv')
        text = text['content']
        text = text[10:11]
        x = predict(text)
        print(str(x))
    '''
