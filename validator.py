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

    total_terms = sum(cluster_tf.values())
    cluster_term_weights = {term: freq / total_terms for term, freq in cluster_tf.items()}

    # Flatten the list of lists into a single list of words
    flat_tokenized_posts = list(chain.from_iterable(tokenized_posts))

    # Collocation extraction using BigramCollocationFinder
    bigram_finder = BigramCollocationFinder.from_words(flat_tokenized_posts)
    bigram_scores = bigram_finder.score_ngrams(BigramAssocMeasures.pmi)

    # Combine significant bigrams with unigrams
    significant_terms = set(term for term, score in bigram_scores) | set(cluster_term_weights.keys())

    # Sort terms by frequency-weighted importance
    sorted_terms = sorted(significant_terms, key=lambda term: cluster_term_weights.get(term, 0), reverse=True)[:n_top_topics]
    return sorted_terms