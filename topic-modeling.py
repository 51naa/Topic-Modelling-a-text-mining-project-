import pickle
import gensim
from sklearn.feature_extraction.text import CountVectorizer

# Load the list of documents
with open('newsgroups', 'rb') as f:
    newsgroup_data = pickle.load(f)

# finding three letter tokens, removing stop_words, 
# removing tokens that don't appear in at least 20 documents,
# removing tokens that appear in more than 20% of the documents
vect = CountVectorizer(min_df=20, max_df=0.2, stop_words='english', 
                       token_pattern='(?u)\\b\\w\\w\\w+\\b')
# Fit and transform
X = vect.fit_transform(newsgroup_data)

# Converting sparse matrix to gensim corpus.
corpus = gensim.matutils.Sparse2Corpus(X, documents_columns=False)

# Mapping from word IDs to words (To be used in LdaModel's id2word parameter)
id_map = dict((v, k) for k, v in vect.vocabulary_.items())

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word=id_map, passes=10)

#Getting 10 topics
ldamodel.print_topics(num_topics=10, num_words=10)

# Naming topics manually based on keywords above
names = ['Automobiles', 'Science', 'Business','Society & Lifestyle', 'Science', 'Education','Computer & IT','Computer & IT','Sports','Sports']

# A function to assess the topic distribution of new texts
def topic_distribution(new_doc):
    
    X_new_doc = vect.transform(new_doc)
    corpus = gensim.matutils.Sparse2Corpus(X_new_doc, documents_columns=False)
    
    
    return list(ldamodel.get_document_topics(corpus))[0]
