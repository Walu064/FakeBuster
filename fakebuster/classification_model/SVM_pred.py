import os
import pandas as pd
from joblib import load


def predict(text: pd.DataFrame) -> int:

    # Wczytanie modelu i vectorizera
    cwd = os.path.dirname(os.path.realpath(__file__))
    clf_loaded = load(f'{cwd}\\svm_model.joblib')
    vectorizer_loaded = load(f'{cwd}\\vectorizer.joblib')

    new_data_transformed = vectorizer_loaded.transform(text)
    predictions = clf_loaded.predict(new_data_transformed)
    return predictions

