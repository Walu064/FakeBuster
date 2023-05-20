import os
import pandas
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Preprocessing requirements:
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
stop_words = set(stopwords.words())
lemmatizer = WordNetLemmatizer()

def preprocess_text(text) -> str:
    global stop_words, lemmatizer
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token.lower() not in stop_words]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    processed_text = ' '.join(tokens)
    return processed_text

test_data_path = os.path.join("..", "..", "test_data_legit_pl.csv")

data_before_preprocessing = pandas.read_csv(test_data_path)["Content"].to_list()
data_frame_fake = pandas.DataFrame(columns=['content'])


for i, ad_content in enumerate(data_before_preprocessing):
    try:
        data_frame_fake.loc[i, :] = [preprocess_text(ad_content)]
    except Exception as e:
        print(e)

output_file_path = os.path.join("..", "data", "learn_legit_data_pl.csv")

data_frame_fake.to_csv(output_file_path)