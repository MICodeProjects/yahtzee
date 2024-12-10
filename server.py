from flask import Flask
from flask import request
from flask import render_template
import os
import sys
from Controllers import Game_Controller, Session_Controller


app = Flask(__name__, static_url_path='', static_folder='static')

#Connect Controller definitions
fpath = os.path.join(os.path.dirname(__file__), 'controllers')
sys.path.append(fpath)
fpath = os.path.join(os.path.dirname(__file__), 'models')
sys.path.append(fpath)

app = Flask(__name__, static_url_path='', static_folder='static')

#The Router section of our application conects routes to Contoller methods
# login pages
app.add_url_rule('/', view_func=Session_Controller.login, methods = ['GET'])
app.add_url_rule('/index', view_func=Session_Controller.login, methods = ['GET'])
app.add_url_rule('/login', view_func=Session_Controller.login, methods = ['GET'])

#app.add_url_rule('/game', view_func=Game_Controller.game, methods = ['POST', 'GET'])
#app.add_url_rule('/fruit/<fruit_name>', view_func=FruitController.single_fruit, methods = ['GET'])

#Start the server
app.run(debug=True, port=5000)

