from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re

lemmatizer = WordNetLemmatizer()

def clean_and_tokenize(text):
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(w) for w in tokens if w.isalpha()]
    return " ".join(tokens)
