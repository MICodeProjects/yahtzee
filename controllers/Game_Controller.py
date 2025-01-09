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
    username=username
    if request.method=="GET":
        if User.exists(username=username)["data"]==False:
            return render_template("login.html", feedback="Username does not exist.")
        
        # get user_info
        user_info=User.get(username=username)["data"]
        
        # get games list
        games_list=Scorecard.get_all_user_game_names(username)["data"]
        high_scores_list=Scorecard.get_high_scores_list(username)["data"]



        return render_template("user_games.html", username=username, user_info=user_info, high_scores_list=high_scores_list, games_list=games_list,feedback="")



def games(): # create new game. requires username and game_name (in little form)
    if request.method=="POST":
        game_name=request.form.get("game_name")
        username=request.form.get("username")
        print(f"game_name: {game_name} \n username: {username}")
        
                
        # get games list
        games_list=Scorecard.get_all_user_game_names(username)["data"]
        high_scores_list=Scorecard.get_high_scores_list(username)["data"]
        print(f"games_list: {games_list}\n high score list: {high_scores_list}")

        # check if game name already exists
        print(f"Checking if game exists... {Game.exists(game_name)}")
        if Game.exists(game_name)["data"]==True:
            return render_template("user_games.html", games_list=games_list, high_scores_list=high_scores_list, feedback="Error......Game name already exists.", username=username)
        


        # check if invalid characters/other errors in game name
        game = Game.create({"name":game_name})
        if game["status"]=="error":
            return render_template("user_games.html", games_list=games_list, high_scores_list=high_scores_list, feedback=str(game["data"]), username=username)

        # create scorecard
        user = User.get(username)
        scorecard=Scorecard.create(game["data"]["id"], user["data"]["id"], f"{game_name}|{username}")
        print(f"creating scorecard...{scorecard}")

        # check if scorecard errors
        if scorecard["status"]=="error":
            return render_template("user_games.html", games_list=games_list, high_scores_list=high_scores_list, username=username, feedback=str(scorecard["data"]))
        print(f"Username is {username}")

        # get user_info
        user_info=User.get(username=username)["data"]

        games_list=Scorecard.get_all_user_game_names(username)["data"]
        high_scores_list=Scorecard.get_high_scores_list(username)["data"]
        print(f"games_list: {games_list}\n high score list: {high_scores_list}")

        return render_template("user_games.html", games_list=games_list, high_scores_list=high_scores_list, username=username, feedback="Game created successfully.")


def game_join(): # join existing game, create scorecard for game
    if request.method=="POST":
        return render_template("user_games.html")

def game_user_delete(username, game_name): # remove user from a game
    if request.method=="GET":
        username=username
        game_name=game_name
        # check if username valid
        if User.exists(username)["data"]==False:
            return render_template("login.html", feedback="Username does not exist")
        elif Game.exists(game_name)["data"]==False:
            return render_template("user_details.html", username=username, feedback="Game does not exist")
        
        print(f"Getting scorecard '{game_name}|{username}'....\n  {Scorecard.get(f"{game_name}|{username}")}")
        scorecard=Scorecard.get(f"{game_name}|{username}")

        print(f"Removing scorecard '{game_name}|{username}'...")
        Scorecard.remove(scorecard["data"]["id"])

        print(f"Removing game {game_name}...")
        Game.remove(game_name)


        return render_template("user_games.html", username=username, high_scores_list=Scorecard.get_high_scores_list(username)["data"], games_list=Scorecard.get_all_user_game_names(username)["data"], feedback=f"Game {game_name} successfully deleted.")

def game_user_game_page(username, game_name): # get specific game for a user
    if request.method=="GET":

        return render_template("game.html", username=username, game_name=game_name)



