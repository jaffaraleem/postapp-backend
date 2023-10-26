from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from bson import json_util
import os
from pymongo.mongo_client import MongoClient

app = Flask(__name__, static_folder='build')
CORS(app)
uri = "mongodb+srv://jaleem:jaffar123@cluster0.aq0mtm8.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)
DB_NAME = "postappdb"
db = client[DB_NAME]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
    
@app.route('/post_data', methods=['POST'])
def post_data():
    data = request.get_json()  
    posts_collection = db.posts
    result = posts_collection.insert_one(data)
    if result.acknowledged:
        return jsonify({"message": "Post added successfully"})
    else:
        return jsonify({"message": "Failed to add post"})

@app.route('/send_data', methods=['GET'])
def send_data():
    posts_collection = db.posts
    posts = list(posts_collection.find({}))
    serialized_posts = json_util.dumps(posts)
    i = 0
    newpost = {}
    for post in posts:
        post["_id"] = i
        newpost[i] = {'text':post["text"],'author':post["author"], 'date':post["date"]}
        i+=1
    return newpost

if __name__ == '__main__':
    app.run()
