from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from bson.errors import InvalidId # For catching InvalidId exception for ObjectId
import os
import json

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_post = int(os.environ.get('MONGO_PORT', '27017'))
# configure the connection to the database
client = MongoClient(mongodb_host, mongodb_post)


# select the databse from mongodb
db = client.list_candidate_VDT

# select the collection (in mongodb the table is called collection)
listCandi = db.candidate


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS']='Content-Type'

def check_empty():
    if listCandi.count_documents({}) > 0:
        print('co du lieu')
    else:
        with open('CLOUD.json') as file:
            file_data = json.load(file)
        print('khong co du lieu')
        listCandi.insert_many(file_data)


@app.route("/")
@app.route("/list", methods=['GET'])
@cross_origin()
def list():
    cursor_candidate = listCandi.find({},{"_id": 0})
    users_list = [user for user in cursor_candidate]
    return jsonify(users_list)
    

if __name__ == "__main__":  # checking if __name__'s value is '__main__'. __name__ is an python environment variable who's value will always be '__main__' till this is the first instatnce of app.py running
    check_empty()
    env = os.environ.get('FLASK_ENV', 'development')
    app.run(debug=True, port=3000, host="0.0.0.0")
