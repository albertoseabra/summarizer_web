import re
import spacy

nlp = spacy.load("en_core_web_md")


def clean_html(text):
    cleaner = re.compile('<.*?>')
    clean_text = re.sub(cleaner, '', text)
    return clean_text


def tokenizing_spacy(text):
    """
    help function to use in the tfidfvectorizer, using spaCy library
    tokenizes the text, removes punctuation and pronouns, and lemmatizes the remaining test
    """
    text = clean_html(text)
    lemmatized_text = []
    for token in nlp(" ".join(text.split("_"))):
        if (token.pos_ == 'PUNCT') | (token.lemma_ == "-PRON-") | (token.pos_ == 'X'):
            continue
        else:
            lemmatized_text.append(token.lemma_)

    return lemmatized_text
