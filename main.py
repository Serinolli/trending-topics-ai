import re
import pymongo
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    return ' '.join([word for word in text.split() if word not in stopwords.words('english')])

client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
db = client["redditscraper"]
posts_collection = db["posts"]

posts_data = posts_collection.find()

post_titles = [post["title"] for post in posts_data]

tokenized_posts = [word_tokenize(clean_text(title)) for title in post_titles]
vectorizer = TfidfVectorizer(max_features=5000)  
X = vectorizer.fit_transform([' '.join(post) for post in tokenized_posts]).toarray()
print(X)
