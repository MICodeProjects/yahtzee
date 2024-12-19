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
        user_info={}
        # user_info["username"]=""
        # user_info["password"]=""
        # user_info["email"]=""
        return render_template("user_details.html", context="create", feedback="")


def single_user(username):
    if request.method=="GET": # get user details page for update/delete
        print(f"args: {request.view_args}")
        print(f"request.query_string {request.url}")
        user = User.get(username=username)
        print(f"user: {user}")
        if user["status"]=="error":
            return render_template("user_details.html", context="update", feedback=str(user["data"]))
        user_info={}
        user_info["username"]=username
        user_info["password"]=user["data"]["password"] # add error recongitintion
        user_info["email"]=user["data"]["email"]
        return render_template("user_details.html", context="update", feedback="", username=user_info["username"], password=user_info["password"], email=user_info["email"])
    
    elif request.method=="POST": # update user
        old_username=username
        new_username=request.form.get("username")
        password=request.form.get("password")
        email=request.form.get("email")
        user_info=User.get(username=old_username)
        if user_info["status"]=="error":
            return render_template("user_details.html", feedback=user_info["data"], context="update")
        User.update({"id":user_info["data"]["id"], "username":new_username, "password":password, "email":email})
        return render_template("user_details.html", username=new_username, context="update", feedback="")
        
# router gets it, then puts it in controller, figures if its get or post, then sends it to 
def user_delete():
    if request.method=="GET":
        username=request.args.get("username")
        User.remove(username)
        return render_template("login.html")
    

