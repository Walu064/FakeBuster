import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.model_selection import train_test_split, GridSearchCV

def accuracy(Y_pred):
    return np.sum(Y_pred == 1)/ len(Y_pred) * 100

# załóżmy, że df to Twój DataFrame, a 'text' to kolumna zawierająca tekst
df = pd.read_csv('E:\Hackathon\supervision2\FakeBuster\samples\data\learn_fake_data.csv')

df = df['content']

# przekształć tekst na numeryczne wektory cech
vectorized = TfidfVectorizer().fit(df)
X = vectorized.transform(df)

# podziel dane na zestaw treningowy i testowy
X_train, X_test = train_test_split(X, test_size=0.2, random_state=23)

# parametry do testowania modelu
parameters = {
    'kernel': ('linear', 'rbf', 'poly', 'sigmoid'),
    'nu': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
    'gamma': ['scale']
}

# uczy model i wybiera najlepsze parametry
# for kernel in parameters['kernel']:
#     for nu in parameters['nu']:
#         for gamma in parameters['gamma']:
#             clf = svm.OneClassSVM(kernel=kernel, nu=nu, gamma=gamma)
#             clf.fit(X_train)
#             y_pred_test = clf.predict(X_test)
#             print("K: "+str(kernel) + ", Nu: "+str(nu) + ", G: "+str(gamma) + ", A: "+str(accuracy(y_pred_test)))

# uczy model na wcześniej określonych parametrach
clf = svm.OneClassSVM(kernel='sigmoid', nu=0.1, gamma='scale')
clf.fit(X_train)
y_pred_test = clf.predict(X_test)
print("A: " + str(accuracy(y_pred_test)) + " fałszywych")


df_test = pd.read_csv('E:\Hackathon\supervision2\FakeBuster\samples\data\learn_legit_data.csv')
# print(df_test)
#
df_test = df_test['content']
#
# przekształć tekst na numeryczne wektory cech
Y = vectorized.transform(df_test)

#
Y_pred = clf.predict(Y)
print("A pred: " + str(accuracy(Y_pred)) + " fałszywych")


