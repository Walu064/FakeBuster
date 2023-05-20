import os
import pandas
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Fake load:
in_fake_file_path = os.path.join("..", "data", "learn_fake_data.csv")
fake_training_data = pandas.read_csv(in_fake_file_path)

fake_training_data_content = fake_training_data['content'].to_list()
fake_training_data_label = ['fake'] * len(fake_training_data_content)

print(fake_training_data_content)

# Legit load:
in_legit_file_path = os.path.join("..", "data", "learn_fake_data.csv")
legit_training_data = pandas.read_csv(in_legit_file_path)

legit_training_data_content = legit_training_data['content'].to_list()
legit_training_data_label = ['legit'] * len(legit_training_data_content)

# Merge of legit and fake data:
merged_content = legit_training_data_content + fake_training_data_content
merged_labels = legit_training_data_label + legit_training_data_content

# Division of data to test and training data:
X_train, X_test, y_train, y_test = train_test_split(merged_content, merged_labels, test_size=0.5, random_state=1000)

# Przetwarzanie danych treningowych
count_vectorizer = CountVectorizer()
X_train_counts = count_vectorizer.fit_transform(X_train)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

# Uczenie klasyfikatora Bayesa na danych treningowych
classifier = MultinomialNB()
classifier.fit(X_train_tfidf, y_train)

# Przetwarzanie danych testowych
X_test_counts = count_vectorizer.transform(X_test)
X_test_tfidf = tfidf_transformer.transform(X_test_counts)

# Klasyfikacja tekstu
predicted_labels = classifier.predict(X_test_tfidf)

# Wyświetlenie wyników klasyfikacji
for text, predicted_label in zip(X_test, predicted_labels):
    print(f"Tekst: {text}")
    print(f"Klasyfikacja: {predicted_label}")
    print()

# Obliczenie dokładności klasyfikatora
accuracy = accuracy_score(y_test, predicted_labels)
print(f"Dokładność klasyfikacji: {accuracy}")