
class Config(object):
    DEBUG = False
    MONGODB_IP = ""
    MONGODB_TEXTS_COLLECTION = ""
    TFIDF_TOKENIZER = "./tokenizer/tfidf_tokenizer.pkl"


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_IP = "mongodb://mongodb:27017/"
    MONGODB_DATABASE = "summarizer_test"
    MONGODB_TEXTS_COLLECTION = "first_test"
    TFIDF_TOKENIZER = "./tokenizer/tfidf_tokenizer.pkl"
    SECRET_KEY = b'_5#y2L"aFs4Q8z\n\xec]/'
