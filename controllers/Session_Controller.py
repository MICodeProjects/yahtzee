from flask import request
from flask import render_template


from models import User_Model
yahtzeeDB_location = './models/yahtzeeDB.db'
User= User_Model.User(yahtzeeDB_location, "users")

def login():
    # curl "http://127.0.0.1:5000"   
    # if user password false: return render template with bad feedback of login.
    if request.method=="GET":
        username=request.args.get("username_input")
        password=request.args.get("password_input")
        print(f"/LOGIN GET. \n  request.url={request.url}, \n  username={username}\n  password={password}")
        if username==None and password==None:
            print(f"No username or password entered. \n  Returning blank template.")
            return render_template("login.html", feedback="")

        print(f"User.exists({username}) running...{User.exists(username=username)}")

        return render_template('user_games.html', username=username, password=password)
            

def index():
    # can send info through route, query string, body
    return render_template('login.html')





