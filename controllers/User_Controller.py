from flask import jsonify
from flask import request
from flask import render_template

from models import User_Model
yahtzeeDB_location = './models/yahtzeeDB.db'
User= User_Model.User_Model(yahtzeeDB_location)


def user_create():
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")
    print(f"request.url={request.args.get('name')}") #GET request & query string
    print(f"request.url={request.form.get('name')}") #POST request & form body
    email=email
    username=username
    password=password
    # for create
    if request.method=="POST":
        User.create({"username":username,"email":email, "password":password})
        return render_template('games.html', username=username)




def user_update():
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")
    print(f"request.url={request.args.get('name')}") #GET request & query string
    print(f"request.url={request.form.get('name')}") #POST request & form body
    email=email
    username=username
    password=password
    # for create
    if request.method=="POST":
        User.update({"username":username,"email":email, "password":password, "id":User.get(username=username)["data"]["id"]})
        return render_template('games.html', username=username)


def single_fruit(fruit_name):
    print(f"request.url={request.url}")
    
    if request.method == 'GET':
        # curl "http://127.0.0.1:5000/fruit/apples"
        all_fruit = Fruit.get_all_fruit()
        if fruit_name in all_fruit:
            fruit = {fruit_name: all_fruit[fruit_name]}
            return jsonify(fruit)
        else:
            return {}