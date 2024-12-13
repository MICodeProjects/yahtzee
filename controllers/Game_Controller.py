from flask import jsonify
from flask import request
from flask import render_template

from models import Game_Model
yahtzeeDB_location = './yahtzeeDB.db'
Game=Game_Model.Game(yahtzeeDB_location, "games")

def games(): # create new game
    name=name
    Game.create({"name":name})
    return render_template("user_games.html")

def game_join(): # join existing game, create scorecard for game
    return render_template("user_games.html")

def game_user_delete(): # remove user from a game
    Game.delete
    return render_template("game.html")

def game_user_game_page(): # get specific game for a user
    return render_template("game.html")

def game_user_page(): # get users game page
    return render_template("user_games.html")


