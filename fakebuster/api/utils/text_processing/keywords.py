import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


SIMILARITY_THRESHOLD = 30

nlp = spacy.load('pl_core_news_lg')

# Preprocessing requirements:
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

def filter_by_query(words : str, query : str) -> bool:
    query = query.split(" ")
    if len(query) == 0:
        return True
    
    doc1 = nlp(str(words))
    doc2 = nlp(str(query))
    similarity_value = doc1.similarity(doc2) * 100
    
    return similarity_value >= SIMILARITY_THRESHOLD


stop_words = set(stopwords.words())
lemmatizer = WordNetLemmatizer()

def get_keywords(text : str) -> list[str]:
    global stop_words, lemmatizer
    
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token.lower() not in stop_words]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return tokens