
class Config(object):
    DEBUG = False
    MONGODB_IP = ""
    MONGODB_TEXTS_COLLECTION = ""
    TFIDF_TOKENIZER = "./tokenizer/tfidf_tokenizer.pkl"


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_IP = ""
    MONGODB_TEXTS_COLLECTION = ""
    TFIDF_TOKENIZER = "./tokenizer/tfidf_tokenizer.pkl"
