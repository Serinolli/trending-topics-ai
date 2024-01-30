import pymongo
from nltk.tokenize import word_tokenize
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from validator import clean_text, GetClusterMainTopics

client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
db = client["redditscraper"]
posts_collection = db["posts"]

posts_data = posts_collection.find()
post_titles = [post["title"] for post in posts_data]

tokenized_posts = [word_tokenize(clean_text(title)) for title in post_titles]

vectorizer = TfidfVectorizer(max_features=5000)  
X = vectorizer.fit_transform([' '.join(post) for post in tokenized_posts]).toarray()

n_clusters = 9
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(X)

cluster_record_counts = {i: 0 for i in range(n_clusters)}
for cluster_label in clusters:
    cluster_record_counts[cluster_label] += 1

sorted_clusters = sorted(cluster_record_counts.items(), key=lambda x: x[1], reverse=True)

main_topics = []
for cluster_id, _ in sorted_clusters:
    main_topics.append(GetClusterMainTopics(cluster_id, post_titles, clusters, tokenized_posts))

for i, topics in enumerate(main_topics):
    print(f"Main topics of Cluster {i}:")
    print(", ".join(topics))
