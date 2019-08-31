# work in progress

### Working with dockerfiles and docker-compose, just need to docker-compose build and run

a web page to create summaries of text    
functionalities planed:    
* different summarization methods
* summarize text based on a url
* summarize text entered directly in the website
* store the original text, summary, date, method used for summarization, etc, in mongodb
* possibility to give feedback of the quality of the summary


## Concepts

### TF-IDF
The Term Frequency – Inverse Document Frequency is very widely used to represent the importance of the words. It tries to reflect how important a word is to a specific document in a corpus. If a word appears a lot in a document but it’s also very common in the remaining documents of the corpus it’s probably not a very important word. But if a word appears a lot in a document and it’s not very common in the corpus that means that this words is especially important for this specific document.

### Word Embeddings

TF-IDF helps us have an idea of the most important words in a text, compared with the corpus, but it says nothing about meaning of the word. Two words can have the same meaning and TF-IDF values completely different. The same goes for sentences, they are a vector of words, two sentences can have almost exactly the same meaning but have completely different vectors. In those cases calculating similarity between the sentences with TF-IDF will fail.
Another problem is the dimensionality of the data, with TF-IDF, like with one hot encoding, we need to have huge sparse vectors to represent our text. If we are working with 100k words we will have a vector of that size for each text where most of the values will be zero because the corresponding word doesnt appear in the text.

Word embeddings solve these problems, each words will be represented by a vector, were the values where learned using a large corpus and are based on the context the words were used. Words used in similar ways, in similar contexts, will have similar representations, that way sentences with similar meaning will also have similar representations.
There are several word embeddings models, Word2Vec and fastText are probably the most popular, they are available to download for free or you can also train your word embeddings with your data using the library Gensim [https://radimrehurek.com/gensim/index.html]
More information about word embeddings:
[https://www.tensorflow.org/tutorials/representation/word2vec]


## Unsupervised Methods

### TextRank[https://www.aclweb.org/anthology/W04-3252] with TF-IDF

For this model we create a graph using the sentences as nodes and the similarity between sentences as the edges weights. This will be a highly connected graph since almost every sentence has some degree of similarity to every other sentence. After this we just need to apply the PageRank algorithm to the graph and we obtain the rank of each sentence, giving us the importance of the sentences in the text.
We can use diferent ways to represent the text and different methods to calculate the similarity between sentences.
In this case i use TF-IDF and cosine similarity.

### Embeddings
The idea in this method is to maximize the similarity between the initial text and the resulting summary, using a greedy approach to select the sentences.
For this i use word embeddings to represent the text. To represent a full sentence, or the full text, i average the word embeddings of the words in the text. This is a simple method to represent the text, but it works well.
There is a very good library to work with NLP, spaCy[https://spacy.io/] ,that does this average of the word embeddings in the text, no need to reinvent the wheel.

### Clustering
This method divides the text in different clusters and selects a sentence from each cluster. The idea is that each cluster will represent a topic/subject in the text giving us a more rich summary, with more diverse information, but with the risk of giving some sentences that are not really relevant in the text.
Uses the same way to represent text as the previous method.