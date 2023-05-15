from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
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
title = "my dream"
heading = "THE ADVENTURE OF VIETTEL DIGITAL TALENT"


app = Flask(__name__)


def check_empty():
    if listCandi.count_documents({}) > 0:
        print('co du lieu')
    else:
        with open('CLOUD.json') as file:
            file_data = json.load(file)
        print('khong co du lieu')
        listCandi.insert_many(file_data)


def redirect_url():
    return request.args.get('next') or \
        request.referrer or \
        url_for('index')


@app.route("/")
@app.route("/list", methods=['GET'])
def list():
    # list all value from a collection
    # todos_l = listCandi.find()
    # print(todos_l)
    todos_l = request.get_data("http://127.0.0.1:3000/list")
    users_list = [user for user in todos_l]
    print(users_list)
    return render_template('index.html',todos=users_list, t=title, h=heading)

# this function use to direct to add a new candicate 
@app.route("/add_candidate")
def add_candidate():
    todos_l = listCandi.find()
    return render_template('add.html', todos=todos_l, t=title, h=heading)


# this function use to direct to remove a new candicate 
@app.route("/remove")
def remove():
    id = request.values.get("_id")
    listCandi.delete_one({"_id": ObjectId(id)})
    return redirect("/")


# this function use to direct to update a new candicate 
@app.route("/update")
def update():
    id = request.values.get("_id")
    candidate = listCandi.find({"_id": ObjectId(id)})
    return render_template('update.html', candidates=candidate, h=heading, t=title)


# this function use to add anew candidate after user click to the button
@app.route("/action", methods=["POST"])
def action_add():
    
    Stt = listCandi.count_documents({}) + 1
    fullname = request.values.get("fullname")
    username = request.values.get("username")
    year = request.values.get("year")
    unversity = request.values.get("university")
    field = request.values.get("field")
    gender = request.values.get("gender")
    listCandi.insert_one({
        "STT": Stt,
        "fullname": fullname,
        "year of birth": year,
        "gender": gender,
        "university": unversity,
        "Username": username,
        "field": field
    })
    return redirect("/add_candidate")


# this function use to update new info of candidate after user click to the button
@app.route("/action_add",  methods=['POST'])
def action_update():
    stt = request.values.get("STT")
    name = request.values.get("name")
    username = request.values.get("Username")
    year=request.values.get("year")
    gender = request.values.get("gender")
    university = request.values.get("university")
    field = request.values.get("field")
    id = request.values.get("_id")
    listCandi.update_one({"_id": ObjectId(id)}, {'$set': {
        "STT": stt,
        "fullname": name,
        "year of birth": year,
        "gender": gender,
        "university": university,
        "Username": username,
        "field": field
    }})
    return redirect("/")


@app.route("/search", methods=["GET"])
def action_search():
    
	key=request.values.get("key")
	refer=request.values.get("refer")
	if(refer=="id"):
		try:
			todos_l = listCandi.find({refer:ObjectId(key)})
			if not todos_l:
				return render_template('index.html',todos=todos_l,t=title,h=heading,error="No such ObjectId is present")
		except InvalidId as err:
			pass
			return render_template('index.html',todos=todos_l,t=title,h=heading,error="Invalid ObjectId format given")
	else:
		todos_l = listCandi.find({refer:key})
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)



if __name__ == "__main__":  # checking if __name__'s value is '__main__'. __name__ is an python environment variable who's value will always be '__main__' till this is the first instatnce of app.py running
    check_empty()
    env = os.environ.get('FLASK_ENV', 'development')
    app.run(debug=True, port=5000, host="0.0.0.0")
