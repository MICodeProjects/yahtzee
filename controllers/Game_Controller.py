from flask import jsonify
from flask import request
from flask import render_template

from models import User_Model
yahtzeeDB_location = './Models/yahtzeeDB.db'
User= User_Model.User_Model(yahtzeeDB_location)


