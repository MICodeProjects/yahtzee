from flask import jsonify
from flask import request
from flask import render_template

from models import User_Model
yahtzeeDB_location = './models/yahtzeeDB.db'
User= User_Model.User(yahtzeeDB_location, "users")


def users():
    # user_info={"username":username,"email":email, "password":password, "id":User.get()}
    if request.method=="POST": # create a user
        username=request.form.get("username")
        password=request.form.get("password")
        email=request.form.get("email")
        print({"username":username,"email":email, "password":password})
        user = User.create({"username":username,"email":email, "password":password})
        print("user create=", user)
        if user["status"]=="error":
            return render_template("user_details.html", context="CREATE", feedback=str(user["data"]))
        return render_template('user_games.html', username=username, feedback="")
    
    if request.method=="GET": # get user details page for create
        user_info={}
        # user_info["username"]=""
        # user_info["password"]=""
        # user_info["email"]=""
        return render_template("user_details.html", context="CREATE", feedback="",username="", password="", email="")


def single_user(username):
    print(f"url=single_user,{request.method}")
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
        return render_template("user_details.html", context="UPDATE", feedback="", username=user_info["username"], password=user_info["password"], email=user_info["email"])
    
    elif request.method=="POST": # update user
        old_username=username
        new_username=request.form.get("username")
        password=request.form.get("password")
        email=request.form.get("email")
        user_info=User.get(username=old_username)

        # check no errors getting the original user info
        if user_info["status"]=="error":
            print(f"  error in getting original user info")
            return render_template("user_details.html", feedback=user_info["data"], context="UPDATE")
        
        user=User.update({"id":user_info["data"]["id"], "username":new_username, "password":password, "email":email})
        print(f"  updated user: {user}")
        if user["status"]=="error":
            print("  ERROR in updated user")
            return render_template("user_details.html", feedback=str(user["data"]), context="UPDATE", username=old_username,password=user_info["data"]["password"], email=user_info["data"]["email"])
        print(" SUCCESS in updating user")
        return render_template("user_details.html", username=new_username, context="UPDATE", feedback="", password=password,email=email)
        
# router gets it, then puts it in controller, figures if its get or post, then sends it to 
def user_delete():
    if request.method=="GET":
        username=request.args.get("username")
        User.remove(username)
        return render_template("login.html", context='UPDATE')
    

