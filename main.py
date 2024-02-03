from nltk.tokenize import word_tokenize
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from validator import clean_text, GetClusterMainTopics
from output import outputClustersInfo
from nltk.tokenize import MWETokenizer
import pymongo
import nltk

nltk.download('stopwords')
nltk.download('punkt')

client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
db = client["redditscraper"]
posts_collection = db["posts"]

posts_data = posts_collection.find()
post_titles = [post["title"] for post in posts_data]

mwe_tokenizer = MWETokenizer()
mwe_tokenizer.add_mwe(('machine', 'learning'))
tokenized_posts = [mwe_tokenizer.tokenize(word_tokenize(clean_text(title))) for title in post_titles]

vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')  
X = vectorizer.fit_transform([' '.join(post) for post in tokenized_posts]).toarray()

non_informative_words = set()
for word, index in vectorizer.vocabulary_.items():
    mean_tfidf_score = X[:, index].mean()
    if mean_tfidf_score < 0.01:
        non_informative_words.add(word)

filtered_tokenized_posts = [[word for word in post if word not in non_informative_words] for post in tokenized_posts]

n_clusters = 9
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(X)

main_topics = []
for cluster_id in range(n_clusters):
    main_topics.append(GetClusterMainTopics(cluster_id, post_titles, clusters, filtered_tokenized_posts))

outputClustersInfo(main_topics)
from nltk.tokenize import word_tokenize
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from validator import clean_text, GetClusterMainTopics
from output import outputClustersInfo
from nltk.tokenize import MWETokenizer
import pymongo
import nltk

nltk.download('stopwords')
nltk.download('punkt')

client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
db = client["redditscraper"]
posts_collection = db["posts"]

posts_data = posts_collection.find()
post_titles = [post["title"] for post in posts_data]

mwe_tokenizer = MWETokenizer()
mwe_tokenizer.add_mwe(('machine', 'learning'))
tokenized_posts = [mwe_tokenizer.tokenize(word_tokenize(clean_text(title))) for title in post_titles]

vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')  
X = vectorizer.fit_transform([' '.join(post) for post in tokenized_posts]).toarray()

non_informative_words = set()
for word, index in vectorizer.vocabulary_.items():
    mean_tfidf_score = X[:, index].mean()
    if mean_tfidf_score < 0.01:
        non_informative_words.add(word)

filtered_tokenized_posts = [[word for word in post if word not in non_informative_words] for post in tokenized_posts]

n_clusters = 9
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(X)

main_topics = []
for cluster_id in range(n_clusters):
    main_topics.append(GetClusterMainTopics(cluster_id, post_titles, clusters, filtered_tokenized_posts))

outputClustersInfo(main_topics)
