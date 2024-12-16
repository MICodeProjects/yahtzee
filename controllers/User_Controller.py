from flask import jsonify
from flask import request
from flask import render_template

from models import User_Model
yahtzeeDB_location = './yahtzeeDB.db'
User= User_Model.User(yahtzeeDB_location, "users")


def users():
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")
    print(f"request.url={request.args.get('username')}") #GET request & query string
    print(f"request.url={request.form.get('username')}") #POST request & form body

    # user_info={"username":username,"email":email, "password":password, "id":User.get()}
    if request.method=="POST": # create a user
        username=request.form.get("username")
        password=request.form.get("password")
        email=request.form.get("email")
        print({"username":username,"email":email, "password":password})
        user = User.create({"username":username,"email":email, "password":password})
        print("user create=", user)
        if user["status"]=="error":
            return render_template("user_details.html", context="create", feedback=str(user["data"]))
        return render_template('user_games.html', username=username, feedback="")
    
    if request.method=="GET": # get user details page for create
        return render_template("user_details.html", context="create", feedback="hello")


def single_user():
    print(f"request.url={request.url}")
    if request.method=="GET": # get user details page for update/delete

        return render_template("user_details.html", context="update")
    
    elif request.method=="POST": # update user
        username=request.args.get("username")
        password=request.args.get("password")
        email=request.args.get("email")
        user_info=User.get(username=username)
        if user_info["status"]=="error":
            return render_template("user_details.html", feedback=user_info["data"], context="update")
        User.update({"id":user_info["data"]["id"], "username":username, "password":password, "email":email})
        return render_template("user_details.html", username=username, context="update")
        
# router gets it, then puts it in controller, figures if its get or post, then sends it to 
def user_delete():
    if request.method=="GET":
        username=request.args.get("username")
        User.remove(username)
        return render_template("login.html")
    

