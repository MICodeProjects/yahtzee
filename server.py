from flask import Flask
from flask import request
from flask import render_template
import os
import sys

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/game')
def game():
    username = request.args.get('username')
    return render_template('game.html', username=username)
    

if __name__ == "__main__":
    port=int(os.environ.get("PORT", 8080))
    app.run(debug=True, port=port)

# #Connect Controller definitions
# fpath = os.path.join(os.path.dirname(__file__), 'controllers')
# sys.path.append(fpath)
# fpath = os.path.join(os.path.dirname(__file__), 'models')
# sys.path.append(fpath)
# from controllers import Game_Controller, Session_Controller

# app = Flask(__name__, static_url_path='', static_folder='static')

# #The Router section of our application conects routes to Contoller methods
# # login pages
# app.add_url_rule('/', view_func=Session_Controller.login, methods = ['GET'])
# app.add_url_rule('/index', view_func=Session_Controller.login, methods = ['GET'])
# app.add_url_rule('/login', view_func=Session_Controller.login, methods = ['GET'])

# # app.add_url_rule('/fruit', view_func=FruitController.fruit, methods = ['POST', 'GET'])
# # app.add_url_rule('/fruit/<fruit_name>', view_func=FruitController.single_fruit, methods = ['GET'])

# #Start the server
# app.run(debug=True, port=5000)

