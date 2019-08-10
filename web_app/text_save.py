from mongoengine import Document, StringField


class TextToStore(Document):
    text = StringField(required=True)
    title = StringField()
    # def __init__(self, text, title, summary, summary_type, summary_size, date, url=None):
    #     self.text = text
    #     self.title = title
    #     self.summary = summary
    #     self.summary_type = summary_type
    #     self.summary_size = summary_size
    #     self.url = url
    #     if url:
    #         self.source = url.split("//")[1].split("/")[0]
    #     self.date = date


