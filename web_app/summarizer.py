from newspaper import Article
import spacy
import numpy as np
from sklearn.cluster import KMeans
import networkx as nx
import re

from utils import tokenizing_spacy

nlp = spacy.load("en_core_web_md")


class Summarizer:
    def __init__(self, tfidf_tokenizer, url=None, text=None):
        self.url = url
        if text:
            self.text = text
            # self.paragraphs = [line for line in self.text.split('\n') if len(line) > 10]

        elif url is not None:
            self.text, self.title = self.scrape_website()
            # self.paragraphs = [line for line in self.text.split('\n') if len(line) > 10]

        else:
            raise Exception('You need a text or a url to summarize')
        self.embedded = nlp(self.text)
        # ignore very short sentences, its very likely its because of some error scrapping the text
        self.sentences = [sentence for sentence in list(self.embedded.sents) if len(sentence) > 10]
        self.sentence_weights = []
        self.tfidf_tokenizer = tfidf_tokenizer

    def scrape_website(self):

        news = Article(self.url)
        news.download()
        news.parse()

        return news.text, news.title

    def doc_embedding_summary(self, number_of_sentences):
        """
        greedy algorithm, selects the sentences, one by one, that create the largest increase in the similarity
        between the full text and the summary
        :param number_of_sentences: how many sentences the summary should contain
        :return: list of the sentences extracted ordered by the same order as they appear in the initial text
        """
        summary_indices = []
        summary = ""
        sentences_simil = []
        # getting the most similar sentence first:
        for i in range(len(self.sentences)):
            sim = self.embedded.similarity(self.sentences[i])
            sentences_simil.append(sim)

        # add it to the summary and to a list of indices of sentences
        summary += str(self.sentences[np.array(sentences_simil).argmax()])
        summary_indices.append(np.array(sentences_simil).argmax())

        while number_of_sentences > 1:
            sentence_to_add = []
            # for each sentence add it to the summary and test the similarity between the new summary and the full text
            # choose the sentence that gives a higher final similarity between text and summary
            for i, sentence in enumerate(self.sentences):
                summary_test = summary + str(sentence)
                similarity_test = self.embedded.similarity(nlp(summary_test))

                if len(sentence_to_add) == 0:
                    sentence_to_add.append((i, similarity_test))
                elif similarity_test > sentence_to_add[0][1]:
                    sentence_to_add[0] = (i, similarity_test)
                else:
                    continue
            summary += str(self.sentences[sentence_to_add[0][0]])
            summary_indices.append(sentence_to_add[0][0])
            number_of_sentences -= 1

        order = sorted(summary_indices)

        return [self.sentences[i] for i in order]

    def clustering_summary(self, number_of_sentences):
        """
        Using clustering: first divides document using K-Means in number_of_sentences clusters
        for each cluster compares the similarity of the full text of the cluster with each sentence that is part of
        that cluster and selects the sentence with the highest similarity with the full text of the custer
        :param number_of_sentences:
        :return:list of the sentences extracted ordered by the same order as they appear in the initial text
        """
        sentences_array = np.array([sentence.vector for sentence in self.sentences])
        cluster = KMeans(number_of_sentences).fit(sentences_array)

        final_summary = []
        # for each cluster creates a text with the sentences that belong to that cluster
        for i, center in enumerate(cluster.cluster_centers_):
            cluster_text = ""
            sentences_indices = []
            for j, sentence in enumerate(self.sentences):
                if cluster.labels_[j] == i:
                    cluster_text += str(self.sentences[j])
                    sentences_indices.append(j)

            # compares the similarity of each sentence with the full text of the cluster
            sentences_simil = []
            cluster_embedding = nlp(cluster_text)
            for indice in sentences_indices:
                sim = self.sentences[indice].similarity(cluster_embedding)
                sentences_simil.append(sim)
            # append to the summary the sentence with the highest similarity
            final_summary.append(sentences_indices[np.array(sentences_simil).argmax()])

        order = sorted(final_summary)

        return [self.sentences[i] for i in order]

    def create_graph(self):
        """
        Creates a graph for the text with the sentences/paragraphs as nodes and
        the similarity between the sentences as the edges
        returns the graph
        """
        # initialize networkx graph
        graph = nx.Graph()

        # iterates of each pair of sentences
        size = len(self.sentences)
        for index1 in range(size):
            for index2 in range(index1 + 1, size):
                if index1 == index2:
                    continue
                # calculates the similarity between the pair of sentences
                # creates and graph edge between the sentences with the similarity as edge weight
                else:
                    graph.add_edge(index1, index2, weight=(self.sentences[index1]).similarity(self.sentences[index2]))

        return graph

    def textrank_summary(self, number_of_sentences):
        """
        Calls the function create_graph to create the graph and calculates the Pagerank value
        of the nodes. Sorts the sentences in descending order of importance
        Prints the most important sentences, depending of the number_sentences
        """
        # better to start with a new weights list every time the summary is called
        self.sentence_weights = []
        # creating the graph
        graph = self.create_graph()
        # calculate Pagerank
        rank = nx.pagerank(graph, weight='weight')

        # convert the rank of sentences to an array
        for v in rank.values():
            self.sentence_weights.append(v)

        # sorting by Rank value
        order = np.array(self.sentence_weights).argsort()[::-1]

        return [self.sentences[i] for i in order]

    def key_words(self, n_words=5):
        """
        prints the most import important n_words from the text
        """
        # stemming and transforming the text first
        # tokens = tokenizing_spacy(self.text)

        vector = self.tfidf_tokenizer.transform([self.text])

        print('The top Words are: ')
        # gets the important stemmed words and find those words in the text to print the original
        words = []
        for index in vector.toarray()[0].argsort()[::-1][:n_words]:
            word = self.tfidf_tokenizer.get_feature_names()[index]

            indices = re.search("{}\S*".format(str(word)), self.text.lower()).span()
            # print(' {};'.format(self.text[indices[0]:indices[1]]), end=' ')
            words.append(self.text[indices[0]:indices[1]])

        return words
