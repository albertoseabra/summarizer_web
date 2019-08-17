from mongoengine import Document, StringField, DateTimeField, \
    IntField, EmbeddedDocument, EmbeddedDocumentField, ListField
from datetime import datetime


class Summary(EmbeddedDocument):
    text = ListField(StringField())
    method = StringField(required=True)
    size = IntField(required=True)
    key_words = ListField(StringField())
    rating = IntField()


class TextToStore(Document):
    meta = {'collection': 'first_test'}

    text = StringField(required=True)
    title = StringField()
    url = StringField()
    source = StringField()
    summary = EmbeddedDocumentField(Summary)
    date = DateTimeField(default=datetime.utcnow)



