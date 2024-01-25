import pymongo
import nltk
import re

nltk.download('corpus')
nltk.download('tokenize')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
db = client["redditscraper"]
posts_collection = db["posts"]

posts_data = [post["title"] for post in posts_collection.find()]
tokenized_posts = [word_tokenize(clean_text(post['title'])) for post in posts_data]

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    return ' '.join([word for word in text.split() if word not in stopwords.words('english')])