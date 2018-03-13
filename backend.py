import os
from flask import Flask, request, jsonify
import pymongo

app = Flask(__name__)
app.debug = True

def mongo_connect():
    url = 'mongodb://genincweather:INFO30005@weather-shard-00-00-hifln.mongodb.net:27017,weather-shard-00-01-hifln.mongodb.net:27017,weather-shard-00-02-hifln.mongodb.net:27017/<DATABASE>?ssl=true&replicaSet=weather-shard-0&authSource=admin'
    client = pymongo.MongoClient(url)
    return client.test_db

def load_from_mongo():
    db = mongo_connect()
    post_list = []
    for post in db.backend_col.find():
        post_list.append(post)
    return post_list[0]['data']

def save_to_mongo(data):
    db = mongo_connect()
    db.backend_col.delete_many({})
    db.backend_col.insert_one({'data': data})

@app.route("/save", methods=['GET', 'POST'])
def save():
    save_to_mongo(request.values.get('data'))
    return jsonify({'message': 'Saved data to MongoDB Cloud.'})

@app.route("/load")
def load():
    return jsonify({'data': load_from_mongo()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)