import re
import pymongo
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from validator import GetClusterMainTopics

# Used functions
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    stop_words = set(stopwords.words('english'))
    return ' '.join(word for word in text.split() if word not in stop_words)    

client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
db = client["redditscraper"]
posts_collection = db["posts"]

posts_data = posts_collection.find()
post_titles = [post["title"] for post in posts_data]

tokenized_posts = [word_tokenize(clean_text(title)) for title in post_titles]

vectorizer = TfidfVectorizer(max_features=5000)  
X = vectorizer.fit_transform([' '.join(post) for post in tokenized_posts]).toarray()

n_clusters = 10
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(X)

main_topics = []
for clusterId in range(n_clusters):
    main_topics.append(GetClusterMainTopics(clusterId, post_titles, clusters[clusterId], tokenized_posts))

for i, topics in enumerate(main_topics):
    print(f"Main topics of Cluster {i}:")
    print(", ".join(topics))