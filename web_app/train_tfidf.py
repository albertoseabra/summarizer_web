from sklearn.feature_extraction.text import TfidfVectorizer


def train_tfidf(corpus, max_words):
    tf = TfidfVectorizer(max_features=max_words)

    tf.fit(corpus)

    return tf


def save_tfidf_tokenizer(path):
    pass


def main():
    pass
    # tf = train_tfidf(corpus, max_features)


if __name__ == '__main__':
    main()
