from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import pandas as pd

import utils


def train_tfidf(corpus, max_words):
    tf = TfidfVectorizer(max_features=max_words,
                         max_df=0.95,
                         min_df=2,
                         tokenizer=utils.tokenizing_spacy,
                         ngram_range=(1, 1))

    tf.fit(corpus)

    return tf


def save_tfidf_tokenizer(tokenizer, path):
    with open(path, 'wb') as f:
        pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)


def main(tokenizer_path, max_words):
    # corpus = ["you need a corpus to train it", "or better, you need a list of corpus to train", "just one more"]

    df = pd.read_csv(r'../data/data.csv', encoding='cp1252')
    corpus = df.text.values
    tf = train_tfidf(corpus, max_words)
    save_tfidf_tokenizer(tokenizer=tf, path=tokenizer_path)


if __name__ == '__main__':
    tokenizer_path = "./tokenizer/tfidf_tokenizer.pkl"
    max_words = 75000
    main(tokenizer_path, max_words)
