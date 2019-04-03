import spacy
import nltk
from string import punctuation
nltk.download("stopwords")
from nltk.corpus import stopwords
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
from spacy.tokenizer import Tokenizer
nlp = spacy.load('en_core_web_sm')
import sklearn
from sklearn.base import TransformerMixin
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS

# Normalizes the text: removes digits and punctuation
def normalizeText(text):
    text = ''.join(c for c in text if not c.isdigit())
    text = ''.join(c for c in text if c not in punctuation).lower()
    return text

# Processes the text: normalizes it and removes stop words
def processText(text):
    text = normalizeText(text)
    STOPLIST = set(stopwords.words('english') + list(ENGLISH_STOP_WORDS))
    text = ' '.join([word for word in text.split() if word not in STOPLIST])
    return text

# Tokenizes the text
def tokenization(text):
    tokenizer = Tokenizer(nlp.vocab)
    tokens = tokenizer(text)
    lemmas = []
    for tok in tokens:
        lemmas.append(tok.lemma_ if tok.lemma_ != "-PRON-" else tok)
    tokens = lemmas
    return tokens

class CleanTextTransformer(TransformerMixin):
    def transform(self, X, **transform_params):
        return [processText(text) for text in X]
    def fit(self, X, y=None, **fit_params):
        return self
    def get_params(self, deep=True):
        return {}