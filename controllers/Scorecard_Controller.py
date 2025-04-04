from flask import jsonify
from flask import request
from flask import render_template

from models import Scorecard_Model
yahtzeeDB_location = './models/yahtzeeDB.db'
Scorecard= Scorecard_Model.Scorecard(yahtzeeDB_location, "scorecards", "users", "games")

def scorecards_update(game_name): # update scorecard
    game_name=game_name
    Scorecard.update(name=game_name)

def game_connection_data(game_name): # given a game name, return all the scorecards in that game
    game_name=game_name
    players = Scorecard.get_all_game_usernames(game_name)
    scorecards = Scorecard.get_all_game_scorecards(game_name)
    print(players["data"], scorecards["data"])


    return jsonify(scorecards["data"])

