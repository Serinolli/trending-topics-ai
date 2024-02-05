import re
from nltk.corpus import stopwords
from itertools import chain
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    stop_words = set(stopwords.words('english'))
    return ' '.join(word for word in text.split() if word not in stop_words)

def GetClusterMainTopics(cluster_id, post_titles, clusters, tokenized_posts, n_top_topics=5):
    cluster_tf = {}
    for i, title in enumerate(post_titles):
        if clusters[i] == cluster_id:
            for term in tokenized_posts[i]:
                cluster_tf[term] = cluster_tf.get(term, 0) + 1

    totalTerms = sum(cluster_tf.values())
    cluster_term_weights = {term: freq / totalTerms for term, freq in cluster_tf.items()}

    flat_tokenized_posts = list(chain.from_iterable(tokenized_posts))
    
    bigramFinder = BigramCollocationFinder.from_words(flat_tokenized_posts)
    bigramScores = bigramFinder.score_ngrams(BigramAssocMeasures.pmi)

    significantTerms = set(term for term, score in bigramScores) | set(cluster_term_weights.keys())

    sortedTerms = sorted(significantTerms, key=lambda term: cluster_term_weights.get(term, 0), reverse=True)[:n_top_topics]
    return sortedTerms