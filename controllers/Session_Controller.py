from flask import request
from flask import render_template


from models import User_Model
from models import Scorecard_Model
yahtzeeDB_location = './models/yahtzeeDB.db'
User= User_Model.User(yahtzeeDB_location, "users")
Scorecard=Scorecard_Model.Scorecard(yahtzeeDB_location, "scorecards", "users","games")

def login():
    # curl "http://127.0.0.1:5000"   
    # if user password false: return render template with bad feedback of login.
    if request.method=="GET":
        username=request.args.get("username")
        password=request.args.get("password")
        print(f"/LOGIN GET. \n  request.url={request.url}, \n  username={username}\n  password={password}")
        if username==None and password==None:
            print(f"No username or password entered. \n  Returning blank template.")
            return render_template("login.html", feedback="", context="LOGIN")

        # check if user exists
        print(f"User.exists({username}) running...{User.exists(username=username)}")
        if User.exists(username=username)["data"]==False:
            return render_template("login.html", feedback="Username does not exist.", context="LOGIN")
        
        # obtaining user
        user=User.get(username=username)["data"]

        # checking password
        print(f"Checking if password for user {user} is correct")
        if user["password"]!=password:
            return render_template("login.html", feedback="Password is incorrect.", context="LOGIN")
        
        return render_template('user_games.html', games_list=Scorecard.get_all_user_game_names(username)["data"], high_scores_list=Scorecard.get_high_scores_list(username)["data"],username=username, password=password, feedback="")
        


            

def index():
    # can send info through route, query string, body
    return render_template('login.html', context="LOGIN")





