from flask import jsonify
from flask import request
from flask import render_template

from models import Scorecard_Model
yahtzeeDB_location = './models/yahtzeeDB.db'
Scorecard= Scorecard_Model.Scorecard(yahtzeeDB_location, "scorecards", "users", "games")

def scorecard_update(): # update scorecard
    return render_template("index.ejs")