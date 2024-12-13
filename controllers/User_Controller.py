from flask import jsonify
from flask import request
from flask import render_template

from models import User_Model
yahtzeeDB_location = './yahtzeeDB.db'
User= User_Model.User(yahtzeeDB_location, "users")


def users():
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")
    print(f"request.url={request.args.get('name')}") #GET request & query string
    print(f"request.url={request.form.get('name')}") #POST request & form body
    email=email

    # user_info={"username":username,"email":email, "password":password, "id":User.get()}
    if request.method=="POST": # create a user
        username=username
        password=password
        email=email
        User.create({"username":username,"email":email, "password":password})
        return render_template('games.html', username=username)
    
    if request.method=="GET": # get user details page for create
        return render_template("user_details.html", context="create")



def single_user():
    print(f"request.url={request.url}")
    if request.method=="GET": # get user details page for update/delete
        username=username
        user_info=User.get(username=username)["data"]
        return render_template("user_details.html", user_info, context="update")
    
    elif request.method=="POST": # update user
        User.update()

        return render_template("user_details.html", username=username,)
        

    
def user_delete():
    User.delete()
    return render_template("login.html")
    

