from flask import jsonify
from flask import request
from flask import render_template

from models import Game_Model
yahtzeeDB_location = './yahtzeeDB.db'
Game=Game_Model.Game(yahtzeeDB_location, "games")

def games(): # create new game
    if request.method=="POST":
        game_name=game_name
        Game.create({"name":game_name})
        return render_template("user_games.html")
    else:
        return render_template("user_games.html")

def game_join(): # join existing game, create scorecard for game
    if request.method=="POST":
        return render_template("user_games.html")

def game_user_delete(): # remove user from a game
    if request.method=="GET":
        return render_template("game.html")

def game_user_game_page(username, game_name): # get specific game for a user
    if request.method=="GET":
        return render_template("game.html")

def game_user_page(): # get users game page
    if request.method=="GET":
        return render_template("user_games.html")


