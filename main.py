import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
db = client["redditscraper"]
posts_collection = db["posts"]

posts_data = [post["title"] for post in posts_collection.find()]