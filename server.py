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

app = Flask(__name__, static_url_path='/public', static_folder='public')

#The Router section of our application conects routes to Contoller methods
app.add_url_rule('/', view_func=Session_Controller.index, methods = ['GET'])
app.add_url_rule('/index', view_func=Session_Controller.index, methods = ['GET'])
app.add_url_rule('/login', view_func=Session_Controller.login, methods = ['GET'])

# users
app.add_url_rule('/users', view_func=User_Controller.users, methods = ['GET','POST']) # get user details page for create/create a user
app.add_url_rule('/users/<username>', view_func=User_Controller.single_user, methods = ['GET','POST']) # update user details
app.add_url_rule('/users/delete/<username>', view_func=User_Controller.user_delete, methods = ['GET'])


# games
app.add_url_rule('/games', view_func=Game_Controller.games, methods = ['POST'])
app.add_url_rule('/games/<username>', view_func=Game_Controller.game_user_page, methods = ['GET'])
app.add_url_rule('/games/join', view_func=Game_Controller.join_game, methods = ['POST'])
app.add_url_rule('/games/delete/<game_name>/<username>', view_func=Game_Controller.game_user_delete, methods = ['GET'])
app.add_url_rule('/games/<game_name>/<username>', view_func=Game_Controller.game_user_game_page, methods = ['GET']) # specific game_name for a user

# scorecards
app.add_url_rule('/scorecards/scorecards_update', view_func=Scorecard_Controller.scorecards_update, methods = ['POST']) # update scorecard
app.add_url_rule('/scorecards/game_connection_data/<game_name>/<username>', view_func=Scorecard_Controller.game_connection_data, methods = ['GET']) # given a game_name, what are all the scorecards associated w/ it?




#Start the server
app.run(debug=True, port=8080)