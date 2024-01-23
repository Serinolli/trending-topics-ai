import pymongo
import re
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split

client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
db = client["redditscraper"]
posts_collection = db["posts"]

posts_data = [post["title"] for post in posts_collection.find()]

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    return ' '.join([word for word in text.split() if word not in stopwords.words('english')])