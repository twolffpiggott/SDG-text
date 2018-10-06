import nltk
import re

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from tqdm import tqdm


def read_combine(train: str, test: str) -> pd.Series:
    """
    Read the train and test set in from csv and combine the text fields for
    preprocessing.

    :param train: filepath to the train set
    :param test: filepath to the test set
    """
    train = pd.read_csv(train, encoding="ISO-8859-1")['Text']
    test = pd.read_csv(test, encoding="ISO-8859-1")['Text']
    return train.append(test)


def prepare_text(text: pd.Series) -> pd.Series:
    """
    Naive approach to text cleaning. Strip out HTML, then do relatively strict
    preparation (lemmatization, stopwords)

    :param text: series of all relevant text data
    """
    # first, remove html tags
    wo_html = text.apply(lambda x: BeautifulSoup(x, "lxml").text)

    tokenizer = RegexpTokenizer(r'\w+')
    stopword_set = set(stopwords.words('english'))
    lmtzr = WordNetLemmatizer()

    clean_text = []
    pbar = tqdm(range(len(text)), desc='clean_text')
    for d in wo_html:
        dlist = d.lower()
        dlist = tokenizer.tokenize(dlist)
        dlist = list(set(dlist).difference(stopword_set))
        # filter tokens
        filtered_tokens = []
        for token in dlist:
            if re.search('^[a-zA-Z]+$', token) and len(token) >= 4:
                filtered_tokens.append(token)
        # lemmatize
        stems = [lmtzr.lemmatize(t) for t in filtered_tokens]
        final_stems = [stem for stem in stems if len(stem) > 3]
        clean_text.append(final_stems)
        pbar.update()
    pbar.close()
    return clean_text


def get_text_indices(text: list, w2i: dict) -> list:
    """
    Turn list of words into list of indices, ignoring words that have been
    excluded from the dictionary.

    :param text: list of words
    :param w2i: dictionary mapping words to indices
    """
    indices = []
    for word in text:
        try:
            indices.append(w2i[word])
        except KeyError as error:
            pass
    return indices


@dataclass
class TextData:
    """
    Class wrapping a bunch of useful attributes for the text we'll be working
    with.

    :attribute cleaned_text: list of list of processed tokens (words)
    :attribute dictionary: set of all unique words
    :attribute w2i: dictionary mapping words to integer indices
    :attribute text_indices: list of lists of words represented by their
                             integer indices
    """
    cleaned_text: list
    limit_words: bool = False
    dictionary: dict = field(init=False, repr=True)
    w2i: dict = field(init=False, repr=True)
    text_indices: list = field(init=False, repr=True)

    def __post_init__(self):
        if self.limit_words:
            word_counts = Counter(w for l in self.cleaned_text for w in l)
            self.dictionary = {w: i for (w, i)
                               in word_counts.most_common(n=10000)}
            print(f'{len(self.dictionary)} unique words identified (limited)')
        else:
            self.dictionary = set(w for l in self.cleaned_text for w in l)
            print(f'{len(self.dictionary)} unique words identified')
        self.w2i = {word: i for i, word in enumerate(self.dictionary)}
        self.text_indices = [get_text_indices(l, self.w2i)
                             for l in self.cleaned_text]


if __name__ == "__main__":
    nltk.download('stopwords')
    nltk.download('wordnet')

    all_text = read_combine('data/Devex_train.csv',
                            'data/Devex_test_questions.csv')
    clean_text = prepare_text(all_text)
    text_data = TextData(clean_text, limit_words=True)
