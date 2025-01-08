from flask import jsonify
from flask import request
from flask import render_template

from models import Game_Model
from models import User_Model
from models import Scorecard_Model

yahtzeeDB_location = './models/yahtzeeDB.db'
Game=Game_Model.Game(yahtzeeDB_location, "games")
User=User_Model.User(yahtzeeDB_location, "users")
Scorecard=Scorecard_Model.Scorecard(yahtzeeDB_location, "scorecards", "users", "games")


def game_user_page(username): # get users game page. basically just the user_games.html page
    if request.method=="GET":
        if User.exists(username=username)["data"]==False:
            return render_template("login.html", feedback="Username does not exist.")
        
        # get user_info
        user_info=User.get(username=username)["data"]
        
        # get games list
        games_list=Scorecard.get_all_user_game_names(username)["data"]
        high_score_list={}





        return render_template("user_games.html", username=username, user_info=user_info, feedback="")



def games(): # create new game. requires username and game_name (in little form)
    if request.method=="POST":
        game_name=request.form.get("game_name")
        username=request.args.get("username")
        print(f"game_name: {game_name} \n username: {username}")
        
        # check if game name already exists
        print(f"Checking if game exists... {Game.exists(game_name)}")
        if Game.exists(game_name)["data"]==True:
            return render_template("user_games.html", feedback="Game name already exists.", username=username)
        
        game = Game.create({"name":game_name})

        # check if invalid characters/other errors
        if game["status"]=="error":
            return render_template("user_games.html", feedback=str(game["data"]), username=username)

        return render_template("user_games.html", feedback="")


def game_join(): # join existing game, create scorecard for game
    if request.method=="POST":
        return render_template("user_games.html")

def game_user_delete(): # remove user from a game
    if request.method=="GET":
        return render_template("game.html")

def game_user_game_page(username, game_name): # get specific game for a user
    if request.method=="GET":
        return render_template("game.html")



