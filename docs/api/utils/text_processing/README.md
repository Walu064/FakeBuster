# Text Processing

## **Description:**

Module for text processing with OCR, NLP implementations.

---

## *Source*

### File: *`keywords.py`*

Get any significat keywords from text input and return

```python
stop_words = set(stopwords.words())
lemmatizer = WordNetLemmatizer()

def get_keywords(text : str) -> list[str]:
    global stop_words, lemmatizer
    
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token.lower() not in stop_words]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return tokens
```

Filter text input with keywords list with `spacy` NLP module and return True if similarity match is greater than SIMILARITY_THRESHOLD

```python
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
```

### File: *`ocr.py`*

Recognize and get text read from image file using OCR pytesseract module.

```python
import pytesseract
from PIL import Image


def get_text_from_img(img : str) -> str:
    image = Image.open(img)
    text = pytesseract.image_to_string(image, lang="pol")
    return text
```
