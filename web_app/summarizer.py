from newspaper import Article
import spacy

nlp = spacy.load("en_core_web_md")


class Summarizer:
    def __init__(self, url=None, text=None):
        self.url = url
        if text:
            self.text = text
            # self.paragraphs = [line for line in self.text.split('\n') if len(line) > 10]

        elif url is not None:
            self.text, self.title = self.scrape_website()
            # self.paragraphs = [line for line in self.text.split('\n') if len(line) > 10]

        else:
            raise Exception('You need a text or a url to summarize')

    def scrape_website(self):

        news = Article(self.url)
        news.download()
        news.parse()

        return news.text, news.title

    def summary(self):

        return self.title, self.text

