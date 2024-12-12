from flask import Flask
from flask import request
import os
import sys

#Connect Controller definitions
fpath = os.path.join(os.path.dirname(__file__), 'controllers')
sys.path.append(fpath)
fpath = os.path.join(os.path.dirname(__file__), 'models')
sys.path.append(fpath)
from controllers import Session_Controller, Game_Controller, Scorecard_Controller, User_Controller

app = Flask(__name__, static_url_path='', static_folder='static')

#The Router section of our application conects routes to Contoller methods
app.add_url_rule('/', view_func=Session_Controller.login, methods = ['GET'])
app.add_url_rule('/index', view_func=Session_Controller.login, methods = ['GET'])
app.add_url_rule('/login', view_func=Session_Controller.login, methods = ['GET'])

app.add_url_rule('/users', view_func=User_Controller.users, methods = ['POST', 'GET'])
app.add_url_rule('/users/<username>', view_func=User_Controller.users, methods = ['GET'])

#Start the server
app.run(debug=True, port=5000)