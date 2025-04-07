import json
from flask import jsonify
from flask import request
from flask import render_template

from models import Scorecard_Model
yahtzeeDB_location = './models/yahtzeeDB.db'
Scorecard= Scorecard_Model.Scorecard(yahtzeeDB_location, "scorecards", "users", "games")

def scorecards_update(): # update scorecard
    print(request.json)
    categories = json.loads(request.json.get("categories"))
    scorecard_name = request.json.get("scorecard_name")
    print(f"categories: {categories}, scorecard_name: {scorecard_name}, type categories {type(categories)}, type scorecard name {type(scorecard_name)}")
    scorecard_id = Scorecard.get(name=scorecard_name)
    if scorecard_id["status"]=="error":
        return {"status":"error", "data":scorecard_id["data"]}
    update = Scorecard.update(id=int(scorecard_id["data"]["id"]), categories=categories)
    if update["status"] == "error":
        return {"status":"error", "data":update["data"]}

    return {"status":"success", "data":"success!"}
    

def game_connection_data(game_name,username): # given a game name, return all the scorecards in that game
    game_name=game_name
    players = Scorecard.get_all_game_usernames(game_name)["data"]
    scorecards = Scorecard.get_all_game_scorecards(game_name)["data"]
    turn_order = Scorecard.get_game_turn_order(game_name)["data"]

    players.remove(username) # remove the current user from tshe list of players
    players.insert(0, username) # add the current user to the front of the list of players

    return json.dumps({"scorecards":scorecards, "players":players, "turn_order":turn_order}) # return all the scorecards and players

